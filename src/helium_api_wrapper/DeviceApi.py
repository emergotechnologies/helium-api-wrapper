"""DeviceAPI module.

.. module:: DeviceApi

:synopsis: Functions to load device data from Helium API

.. moduleauthor:: DSIA21

"""

import logging
from typing import Optional

from helium_api_wrapper.DataObjects import Device
from helium_api_wrapper.DataObjects import Event
from helium_api_wrapper.Endpoint import Endpoint


logging.basicConfig(level=logging.INFO)


class DeviceApi:
    """Class to describe Device API."""

    logger: logging.Logger

    def __init__(self, logger: Optional[logging.Logger] = None):
        self.logger: logging.Logger = logger or logging.getLogger(__name__)

    def get_endpoint(
        self, endpoint_url: str = "devices", response: Optional[Device] = Device
    ) -> Endpoint:
        """Load the Device data.

        :param endpoint_url: The url of the endpoint, defaults to "hotspots"
        :type: str, optional

        :param params: The parameters to send with the request, defaults to {}
        :type: dict, optional

        :param response: The type of the data, defaults to None
        :type: DataObject, optional

        :return: The endpoint.
        :rtype: Endpoint
        """
        endpoint = Endpoint(
            name=endpoint_url,
            params={},
            response_type=response,
            type="console",
        )
        return endpoint

    def get_device(self, uuid: str) -> Device:
        """Get a device by its uuid.

        :param uuid: The ID of the Device, defaults to None
        :type uuid: str

        :return: The Device.
        :rtype: Device
        """
        self.logger.info(f"Getting Device for uuid {uuid}")
        endpoint = self.get_endpoint(f"devices/{uuid}")
        endpoint.request_with_exponential_backoff()
        return endpoint.data[0]

    def get_integration_events(self, uuid: str) -> Event:
        """Get the previous 10 Integration events for the device with the given uuid.

        :param uuid: The ID of the Device, defaults to None
        :type uuid: str

        :return: The Event.
        :rtype: Event
        """
        self.logger.info(f"Getting Device Integration Events for uuid {uuid}")
        endpoint = self.get_endpoint(
            f"devices/{uuid}/events?sub_category=uplink_integration_req"
        )
        endpoint.request_with_exponential_backoff()
        return endpoint.data

    def get_events(self, uuid: str) -> Event:
        """Get the previous 100 events for the device with the given uuid.

        :param uuid: The ID of the Device, defaults to None
        :type uuid: str

        :return: The Event.
        :rtype: Event
        """
        self.logger.info(f"Getting Device Events for uuid {uuid}")
        endpoint = self.get_endpoint(f"devices/{uuid}/events")
        endpoint.request_with_exponential_backoff()
        return endpoint.data
