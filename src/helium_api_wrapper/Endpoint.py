"""Endpoint Module.

.. module:: Endpoint

:synopsis: Classes and functions for Helium API Endpoint

.. moduleauthor:: DSIA21

"""

import logging
import os
import time
from pydantic import Field
from typing import Any, Union
from typing import Dict
from typing import List
from typing import Optional
from typing import Type

import requests
from dotenv import find_dotenv
from dotenv import load_dotenv
from requests import Response

from helium_api_wrapper.DataObjects import DataObject


logging.basicConfig(level=logging.INFO)


class Endpoint(DataObject):
    # type: ignore[misc]
    # TODO: check if this causes problems, I changed it from a dataclass to a DataObject
    """An endpoint for the Helium API."""

    name: str
    method: str = "GET"
    params: Dict[str, str] = Field(default_factory=dict)
    response_type: Type[DataObject]
    response_code: Optional[int] = None
    headers: Dict[str, str] = Field(default_factory=dict)
    error_codes: List[int] = Field(default_factory=lambda: [429, 500, 502, 503])
    data: List[DataObject] = Field(default_factory=list)
    cursor: Optional[str] = None
    logger: logging.Logger = logging.getLogger(__name__)
    type: str = "blockchain"

    def get_url(self) -> str:
        """Get the URL for the endpoint.

        :return: The URL for the endpoint.
        """
        ts = ".1"  # int(time.time())
        if self.type == "blockchain":
            self.headers = {"User-Agent": f"HeliumPythonWrapper/0.3{ts}"}
            # self.headers = {
            #     "User-Agent": "Mozilla/5.0."
            # }
            return f"https://api.helium.io/v1/{self.name}"
        else:
            # if package is installed globally look for .env in cwd
            if not (dotenv_path := find_dotenv()):
                dotenv_path = find_dotenv(usecwd=True)

            load_dotenv(dotenv_path)
            api_key = os.getenv("API_KEY")

            if not api_key:
                self.logger.error(
                    "No API_KEY key found, please provide one as env variable or .env file"
                )
                raise RuntimeError(
                    "No API_KEY key found, please provide one as env variable or .env file"
                )
            self.headers = {
                "User-Agent": f"HeliumPythonWrapper/0.3{ts}",
                "key": api_key,
            }
            return f"https://console.helium.com/api/v1/{self.name}"

    def __request(self) -> Response:
        """Send a simple request to the Helium API and return the response."""
        self.logger.debug(f"Requesting {self.name}...")
        response = requests.request(
            self.method,
            self.get_url(),
            params=self.params,
            headers=self.headers,
        )
        return response

    def request_with_exponential_backoff(self, max_retries: int = -1) -> None:
        """Send a request and retry with exponential backoff.

        if the response code is in the error_codes list.

        :param max_retries: The maximum number of retries. -1 means infinite retries.
        :type max_retries: int
        :return: None
        """
        response = self.__request()
        self.response_code = response.status_code
        exponential_sleep_time = 1
        num_of_retries = 0
        is_error = self.response_code in self.error_codes
        while (is_error and max_retries == -1) or (
            is_error and num_of_retries < max_retries
        ):
            num_of_retries += 1
            self.logger.info(
                f"Got status code {self.response_code} on {self.get_url()}. Sleeping for {exponential_sleep_time} seconds"
            )
            exponential_sleep_time = min(600, exponential_sleep_time * 2)
            time.sleep(exponential_sleep_time)
            response = self.__request()
            self.response_code = response.status_code
            is_error = self.response_code in self.error_codes

        if self.response_code in self.error_codes:
            raise Exception(
                f"Request to {self.get_url()} failed with status code {self.response_code}"
            )
        else:
            self.__handle_response(response)

    def crawl_pages(self, page_amount: int = 10) -> None:
        """Gets the result pages.

        This function allows user to read next pages of results and save them to the dataframe
        :return: None
        """
        for page in range(page_amount):
            self.request_with_exponential_backoff()
            if self.cursor is None:
                self.logger.debug(
                    f"Finished crawling data at page {page + 1} of {page_amount}."
                )
                break
            self.logger.debug(f"Page {page + 1} of {page_amount} crawled.")

    def add_cursor_to_params(self) -> None:
        """Add the hash to the params."""
        if self.cursor is not None:
            self.params["cursor"] = self.cursor

    def __handle_response(self, response: requests.Response) -> None:
        """Handle the response from the Helium API."""
        if self.response_code == 404:
            self.logger.warning("Resource not found")
            return

        if self.response_code == 204:
            self.logger.warning("No content")
            return
        else:
            r = response.json()

        if self.response_code == 200:
            if "cursor" in r:
                self.cursor = r["cursor"]
                self.add_cursor_to_params()

            # @todo: find better way to handle this (maybe use subclasses)
            if self.type == "blockchain":
                if "data" not in r:
                    raise Exception("No data received.")

                if isinstance(r["data"], list):
                    self.data.extend(
                        [self.__resolve_response_type(i) for i in r["data"]]
                    )
                else:
                    self.data.append(self.__resolve_response_type(r["data"]))
            else:
                if isinstance(r, list):
                    self.data.extend([self.__resolve_response_type(i) for i in r])
                else:
                    self.data.append(self.__resolve_response_type(r))

            return self.data
        else:
            raise Exception(
                f"Request to {self.get_url()} failed with status code {self.response_code}"
            )

    def __resolve_response_type(
            self, data: Dict[str, str]
    ) -> Union[DataObject, Dict[str, str]]:
        """Resolve the response type.

        :param data: The data from the response.
        :type data: dict

        :return: The response type.
        """
        if self.response_type is None:
            self.logger.debug("No response type specified. Returning raw data.")
            return data
        else:
            return self.response_type(**data)
