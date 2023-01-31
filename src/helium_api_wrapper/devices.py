"""Device Module.

.. module:: helpers

:synopsis: Functions to load Devices from Helium API

.. moduleauthor:: DSIA21

"""

import logging
from typing import List

from helium_api_wrapper.DataObjects import Device
from helium_api_wrapper.DataObjects import Event
from helium_api_wrapper.DataObjects import IntegrationEvent
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


def get_last_integration(uuid: str) -> IntegrationEvent:
    """Load a device integration events.

    :param uuid: UUID of the device
    :return: Device
    """
    logger.info(f"Getting Device Integration Events for uuid {uuid}")
    events = request(
        url=f"devices/{uuid}/events?sub_category=uplink_integration_req",
        endpoint="console",
    )

    if len(events) == 0:
        raise Exception(f"No Integration Events existing for device with uuid {uuid}")

    last_event = None
    hotspots = []

    # Handling too long body
    for event in events:
        if isinstance(event["data"]["req"]["body"], str):
            continue
        last_event = event
        break

    if last_event is None:
        raise Exception(f"No Integration Events existing for device with uuid {uuid}")

    if len(last_event["data"]["req"]["body"]["hotspots"]) == 0:
        raise Exception(
            f"No Hotspots existing for integration of device with uuid {uuid}"
        )

    for hotspot in last_event["data"]["req"]["body"]["hotspots"]:
        hsp = get_hotspot_by_address(hotspot["id"])
        if len(hsp) == 0:
            logger.info(f"No Hotspot found for address {hotspot['id']}")
            continue
        else:
            h = hsp[0].dict()
            h["rssi"] = hotspot["rssi"]
            h["snr"] = hotspot["snr"]
            h["datarate"] = hotspot["spreading"]
            h["frequency"] = hotspot["frequency"]
            h["reported_at"] = hotspot["reported_at"]
            # h["status"] = hotspot["snr"]
            hotspots.append(IntegrationHotspot(**h))

    last_event["hotspots"] = hotspots

    return IntegrationEvent(**last_event)


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
