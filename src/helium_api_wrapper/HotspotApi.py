"""HotspotApi module.

.. module:: HotspotApi

:synopsis: Functions to load the hotspot data from Helium API

.. moduleauthor:: DSIA21

"""

import logging
from typing import List
from typing import Union

from helium_api_wrapper.DataObjects import DataObject
from helium_api_wrapper.DataObjects import Hotspot
from helium_api_wrapper.DataObjects import Role
from helium_api_wrapper.Endpoint import Endpoint


logging.basicConfig(level=logging.INFO)


class HotspotApi:
    """Class to describe Hotspot API."""

    def __init__(self, logger: logging.Logger = None):
        if logger is None:
            self.logger = logging.getLogger(__name__)
        else:
            self.logger = logger

    def get_endpoint(
        self, endpoint_url="hotspots", params=None, response: DataObject = Hotspot
    ) -> Endpoint:
        """Load the hotspot data.

        :param endpoint_url: The url of the endpoint, defaults to "hotspots"
        :type endpoint_url: str, optional

        :param params: The parameters to send with the request, defaults to {}
        :type params: dict, optional

        :param response: The type of the data, defaults to Hotspot
        :type response: DataObject, optional

        :return: The endpoint.
        :rtype: Endpoint
        """
        if params is None:
            params = {}
        endpoint = Endpoint(endpoint_url, "GET", params, response_type=response)
        return endpoint

    def get_hotspot_by_address(self, address: str) -> Union[Hotspot, None]:
        """Get a hotspot by address.

        :param address: The address of the hotspot, defaults to None
        :type address: str

        :return: The hotspot.
        :rtype: Hotspot
        """
        self.logger.info(f"Getting hotspot for adress {address}")
        endpoint = self.get_endpoint(f"hotspots/{address}")
        endpoint.request_with_exponential_backoff()
        if len(endpoint.data) == 0:
            return None
        else:
            return endpoint.data[0]

    def get_hotspots(
        self, page_amount: int = 10, filter_modes: str = "full"
    ) -> List[Hotspot]:
        """Get a list of hotspots.

        :return: The hotspots.
        :rtype: list[Hotspot]
        """
        self.logger.info("Getting hotspots")

        endpoint = self.get_endpoint(params={"filter_modes": filter_modes})
        endpoint.crawl_pages(page_amount=page_amount)
        return endpoint.data

    def get_hotspots_by_addresses(self, addresses: list) -> List[Hotspot]:
        """Get a list of hotspots.

        :return: The hotspots.
        :rtype: list[Hotspot]
        """
        self.logger.info("Getting hotspots for addresses")
        hotspots = []
        for adress in addresses:
            hotspots.append(self.get_hotspot_by_address(adress))
        return hotspots

    def get_hotspots_by_position(
        self, lat: float, lon: float, distance: int
    ) -> List[Hotspot]:
        """Get a list of hotspots by position.

        :param lat: The latitude of the position, defaults to None
        :type lat: float

        :param lon: The longitude of the position, defaults to None
        :type lon: float

        :param distance: The distance in meters, defaults to None
        :type distance: int

        :return: The hotspots.
        :rtype: list[Hotspot]
        """
        self.logger.info(
            f"Getting hotspots for position {lat}, {lon} within {distance} meters"
        )
        endpoint = self.get_endpoint(
            "hotspots/location/distance",
            params={"lat": lat, "lon": lon, "distance": distance},
        )
        endpoint.crawl_pages(page_amount=10)
        return endpoint.data

    def get_hotspots_box_search(
        self, swlat: float, swlon: float, nelat: float, nelon: float
    ) -> List[Hotspot]:
        """Get a list of hotspots by box search.

        :param swlat: The latitude of the southwest corner, defaults to None
        :type swlat: float

        :param swlon: The longitude of the southwest corner, defaults to None
        :type swlon: float

        :param nelat: The latitude of the northeast corner, defaults to None
        :type nelat: float

        :param nelon: The longitude of the northeast corner, defaults to None
        :type nelon: float

        :return: The hotspots.
        :rtype: list[Hotspot]
        """
        self.logger.info(
            f"Getting hotspots for box search {swlat}, {swlon}, {nelat}, {nelon}"
        )
        endpoint = self.get_endpoint(
            "hotspots/location/box_search",
            params={"swlat": swlat, "swlon": swlon, "nelat": nelat, "nelon": nelon},
        )
        endpoint.crawl_pages(page_amount=10)
        return endpoint.data

    def get_hotspot_roles(
        self, address: str, limit: int, filter_types: str = ""
    ) -> List[Role]:
        """Get a list of hotspots by owner.

        :param address: The address of the owner, defaults to None
        :type address: str

        :param limit: The amount of roles to return, defaults to None
        :type limit: int

        :param filter_types: The types of roles to return, defaults to ""
        :type filter_types: str, optional

        :return: The hotspots.
        :rtype: list[Role]
        """
        self.logger.info(f"Getting hotspot roles for {address}")

        params = {}

        if filter_types != "":
            params["filter_types"] = filter_types

        if limit < 0:
            raise ValueError("Limit must be greater than 0")
        else:
            params["limit"] = limit

        endpoint = self.get_endpoint(
            f"hotspots/{address}/roles", params=params, response=Role
        )
        endpoint.crawl_pages(page_amount=1)
        if endpoint.data is None:
            raise ValueError("No recent roles found")
        return endpoint.data
