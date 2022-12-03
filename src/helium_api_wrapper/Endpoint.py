"""Endpoint Module.

.. module:: Endpoint

:synopsis: Classes and functions for Helium API Endpoint

.. moduleauthor:: DSIA21

"""

import logging
import time
from typing import Dict
from typing import List
from typing import Optional
from typing import Type

import requests
from pydantic import BaseModel
from requests import Response


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Endpoint:  # TODO: check if this causes problems, I changed it from a dataclass to a DataObject
    """An endpoint for the Helium API."""

    url: str
    response_type: Type[BaseModel]
    response_code: Optional[int]
    headers: Dict[str, str]
    params: Dict[str, str]
    error_codes: List[int]
    data: List[BaseModel]
    cursor: Optional[str]

    def __init__(
        self,
        url: str,
        response_type: Type[BaseModel],
        response_code: Optional[int] = None,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, str]] = None,
        error_codes: Optional[List[int]] = None,
        cursor: Optional[str] = None,
    ) -> None:
        self.url = url
        self.response_type = response_type
        self.response_code = response_code
        self.headers = headers or {"User-Agent": "HeliumPythonWrapper/0.3.1"}
        self.params = params or {}
        self.error_codes = error_codes or [429, 500, 502, 503]
        self.cursor = cursor
        self.data = []

    def request_with_exponential_backoff(self, max_retries: int = -1) -> None:
        """Send a request and retry with exponential backoff.

        if the response code is in the error_codes list.

        :param max_retries: The maximum number of retries. -1 means infinite retries.
        :type max_retries: int
        :return: None
        """
        print(self.url)
        response = request(url=self.url, headers=self.headers, params=self.params)
        self.response_code = response.status_code
        exponential_sleep_time = 1
        num_of_retries = 0
        is_error = self.response_code in self.error_codes
        while (is_error and max_retries == -1) or (
            is_error and num_of_retries < max_retries
        ):
            num_of_retries += 1
            logger.info(
                f"Got status code {self.response_code} on {get_url(url=self.url)}. "
                f"Sleeping for {exponential_sleep_time} seconds"
            )
            exponential_sleep_time = min(600, exponential_sleep_time * 2)
            time.sleep(exponential_sleep_time)
            response = request(
                url=self.url,
                headers=self.headers,
                params=self.params,
            )
            self.response_code = response.status_code
            is_error = self.response_code in self.error_codes

        if self.response_code in self.error_codes:
            raise Exception(
                f"Request to {get_url(url=self.url)} failed with status code {self.response_code}"
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
                logger.debug(
                    f"Finished crawling data at page {page + 1} of {page_amount}."
                )
                break
            logger.debug(f"Page {page + 1} of {page_amount} crawled.")

    def __handle_response(self, response: requests.Response) -> None:
        """Handle the response from the Helium API."""
        if self.response_code == 404:
            logger.warning("Resource not found")
            return

        if self.response_code == 204:
            logger.warning("No content")
            return
        else:
            r = response.json()

        if self.response_code == 200:
            if "cursor" in r:
                cursor: str = r["cursor"]
                self.cursor = cursor
                self.params["cursor"] = cursor

            if "data" not in r:
                raise Exception("No data received.")

            if isinstance(r["data"], list):
                self.data.extend([self.response_type(**i) for i in r["data"]])
            else:
                self.data.append(self.response_type(**r["data"]))

        else:
            raise Exception(
                f"Request to {get_url(url=self.url)} failed with status code {self.response_code}"
            )


# TODO: make private
def request(url: str, params: Dict[str, str], headers: Dict[str, str]) -> Response:
    """Send a simple request to the Helium API and return the response."""
    logger.debug(f"Requesting {url}...")
    response = requests.request(
        "GET",
        get_url(url=url),
        params=params,
        headers=headers,
    )
    return response


# TODO: make private
def get_url(url: str) -> str:
    """Get the URL for the endpoint.

    :return: The URL for the endpoint.
    """
    return f"https://api.helium.io/v1/{url}"
