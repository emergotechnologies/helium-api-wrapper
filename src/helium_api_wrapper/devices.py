"""Device Module.

.. module:: helpers

:synopsis: Functions to load Devices from Helium API

.. moduleauthor:: DSIA21

"""

import logging
from typing import List

from helium_api_wrapper.DataObjects import Device
from helium_api_wrapper.DataObjects import Event
from helium_api_wrapper.DataObjects import IntegrationHotspot
from helium_api_wrapper.endpoint import request
from helium_api_wrapper.hotspots import get_hotspot_by_address


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_device_by_uuid(uuid: str) -> Device:
    """Load a device.

    :param uuid: UUID of the device
    :return: Device
    """
    logger.info(f"Getting Device for uuid {uuid}")
    device = request(url=f"devices/{uuid}", endpoint="console")
    try:
        return Device(**device[0])
    except IndexError:
        logger.info(f"No Device found for uuid {uuid}")
        return Device(uuid=uuid)


def get_last_integration(uuid: str) -> Event:
    """Load a device integration events.

    :param uuid: UUID of the device
    :return: Device
    """
    logger.info(f"Getting Device Integration Events for uuid {uuid}")
    event = request(
        url=f"devices/{uuid}/events?sub_category=uplink_integration_req",
        endpoint="console",
    )
    event = event[0]
    hotspots = []

    for hotspot in event["data"]["req"]["body"]["hotspots"]:
        h = get_hotspot_by_address(hotspot["id"])[0].dict()
        h["rssi"] = hotspot["rssi"]
        h["snr"] = hotspot["snr"]
        h["spreading"] = hotspot["spreading"]
        h["frequency"] = hotspot["frequency"]
        h["reported_at"] = hotspot["reported_at"]
        h["status"] = hotspot["snr"]
        hotspots.append(IntegrationHotspot(**h))

    event["hotspots"] = hotspots

    try:
        return Event(**event)
    except IndexError:
        logger.info(f"No Integration Events existing for device with uuid {uuid}")
        return Event(device_id=uuid)


def get_last_event(uuid: str) -> Event:
    """Load a device event.

    :param uuid: UUID of the device
    :return: Device
    """
    logger.info(f"Getting Device Event for uuid {uuid}")
    events = get_events_for_device(uuid)
    print(events)
    try:
        return events[0]
    except IndexError:
        logger.info(f"No Events existing for device with uuid {uuid}")
        return Event(device_id=uuid)


def get_events_for_device(uuid: str) -> List[Event]:
    """Get the previous 100 events for the device with the given uuid.

    :param uuid: The ID of the Device, defaults to None
    :type uuid: str

    :return: The Event.
    :rtype: Event
    """
    logger.info(f"Getting Device Events for uuid {uuid}")
    events = request(url=f"devices/{uuid}/events", endpoint="console")
    if len(events) == 0:
        logger.info(f"No Events existing for device with uuid {uuid}")
    return [Event(**event) for event in events]
