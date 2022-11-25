"""
.. module:: Endpoint

:synopsis: Classes and functions for Helium API Endpoint

.. moduleauthor:: DSIA21

"""

import os
from dataclasses import dataclass, field
import logging
import time
from typing import List, Type, Union
from dotenv import load_dotenv, find_dotenv

import requests
from requests import Response

from helium_api_wrapper.DataObjects import DataObject
from pydantic import Field, BaseModel

logging.basicConfig(level=logging.INFO)


@dataclass
class Endpoint:
    """ An endpoint for the Helium API.

        :param name: The name of the endpoint, defaults to None
        :type name: str
        :example name: "hotspots/11cxkqa2PjpJ9YgY9qK3Njn4uSFu6dyK9xV8XE4ahFSqN1YN2db"

        :param method: The HTTP method to use, defaults to None
        :type method: str
        :example method: "GET"

        :param params: The parameters to send with the request, defaults to None
        :type params: dict, optional
        :example params: {'address': '11cxkqa2PjpJ9YgY9qK3Njn4uSFu6dyK9xV8XE4ahFSqN1YN2db'}

        :param headers: The headers to send with the request, defaults to None
        :type headers: dict, optional
        :example headers: {'Accept': 'application/json'}

        :param response_type: The type of the response, defaults to None
        :type response_type: DataObject, optional
        :example response_type: Hotspot

        :param page_amount: The amount of pages to crawl, defaults to 1
        :type page_amount: int, optional
        :example page_amount: 10

        :param error_codes: The error codes to retry on, defaults to [429, 500, 502, 503, 504]
        :type error_codes: list, optional
        :example error_codes: [429, 500, 502, 503, 504]

        :param data: The data from the response, defaults to []
        :type data: list[DataObject], optional
        :example data: [Hotspot, Hotspot, Hotspot]

        :param hash: The hash of the next page, defaults to None
        :type hash: str, optional
    """
    name: str
    # url: str
    method: str = "GET"
    _params: dict = None
    # response: dict = None
    response_type: Type[DataObject] = None
    response_code: int = None
    headers: dict = None
    error_codes: List[int] = field(default_factory=lambda: [429, 500, 502, 503])
    data: List[DataObject] = field(default_factory=list)
    cursor: str = None
    logger = logging.getLogger(__name__)
    type: str = "blockchain"

    def get_url(self) -> str:
        """Get the URL for the endpoint.

        :return: The URL for the endpoint.
        """
        ts = ".1" #int(time.time())
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

            assert api_key, "No api key found in .env. The helium console api requires an api key."
            self.headers = {
                "User-Agent": f"HeliumPythonWrapper/0.3{ts}",
                "key": os.getenv("API_KEY")
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
        """ Send a request and retry with exponential backoff
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
        while (is_error and max_retries == -1) or (is_error and num_of_retries < max_retries):
            num_of_retries += 1
            self.logger.info(
                f"Got status code {self.response_code} on {self.get_url()}. Sleeping for {exponential_sleep_time} seconds")
            exponential_sleep_time = min(600, exponential_sleep_time * 2)
            time.sleep(exponential_sleep_time)
            response = self.__request()
            self.response_code = response.status_code
            is_error = self.response_code in self.error_codes

        if self.response_code in self.error_codes:
            raise Exception(f"Request to {self.get_url()} failed with status code {self.response_code}")
        else:
            self.__handle_response(response)

    def crawl_pages(self, page_amount=10) -> None:
        """ Gets the result pages

            This function allows user to read next pages of results and save them to the dataframe
            :return: None
        """
        for page in range(page_amount):
            self.request_with_exponential_backoff()
            if self.cursor is None:
                self.logger.debug(f"Finished crawling data at page {page + 1} of {page_amount}.")
                break
            self.logger.debug(f"Page {page + 1} of {page_amount} crawled.")

    @property
    def params(self) -> dict:
        """ Returns the params for the request. """
        return self._params

    @params.setter
    def params(self, value) -> None:
        """Set the params for the request."""
        # z = x | y
        self._params = value

    def add_cursor_to_params(self) -> None:
        """Add the hash to the params."""
        if self.cursor is not None:
            self.params["cursor"] = self.cursor

    def __handle_response(self, response) -> Union['data', Exception]:
        """Handle the response from the Helium API.

        :return: The data from the response.
        """

        if self.response_code == 404:
            self.logger.warning("Ressource not found")
            return None

        if self.response_code == 204:
            self.logger.warning("No content")
            return None
        else:
            r = response.json()

        if self.response_code == 200:
            if "cursor" in r:
                self.cursor = r["cursor"]
                self.add_cursor_to_params()

            # @todo: find better way to handle this (maybe use subclasses)
            if self.type =="blockchain":
                if "data" not in r:
                    raise Exception("No data received.")

                if isinstance(r["data"], list):
                    self.data.extend([self.__resolve_response_type(i) for i in r["data"]])
                else:
                    self.data.append(self.__resolve_response_type(r["data"]))
            else:
                if isinstance(r, list):
                    self.data.extend([self.__resolve_response_type(i) for i in r])
                else:
                    self.data.append(self.__resolve_response_type(r))

            return self.data
        else:
            raise Exception(f"Request to {self.get_url()} failed with status code {self.response_code}")

    def __resolve_response_type(self, data:dict) -> Union[Type[DataObject], dict]:
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
