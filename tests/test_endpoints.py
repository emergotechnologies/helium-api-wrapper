"""Test cases for Endpoints."""
import json

import pytest

from helium_api_wrapper import challenges as challenges
from helium_api_wrapper import devices as devices
from helium_api_wrapper import hotspots as hotspots
from helium_api_wrapper.DataObjects import Challenge, Device, Event
from helium_api_wrapper.DataObjects import Hotspot


@pytest.fixture
def mock_hotspots():
    with open("./data/hotspots.json") as file:
        hotspot = json.load(file)
    return hotspot


@pytest.fixture
def mock_challenges():
    with open("./data/challenges.json") as file:
        challenge = json.load(file)
    return challenge


@pytest.fixture
def mock_devices():
    with open("./data/devices.json") as file:
        device = json.load(file)
    return device


@pytest.fixture
def mock_integrations():
    with open("./data/integration_events.json") as file:
        integration = json.load(file)
    return integration


@pytest.fixture
def mock_events():
    with open("./data/events.json") as file:
        event = json.load(file)
    return event


"""Test cases for HotspotApi."""


def test_get_hotspot_succeeds(mocker, mock_hotspots) -> None:
    """It exits with a status code of zero."""
    mocker.patch(
        "helium_api_wrapper.hotspots.get_hotspot_by_address",
        return_value=Hotspot(**mock_hotspots[0]),
        autospec=True,
    )

    result = hotspots.get_hotspot_by_address(address="some_address")
    assert type(result).__name__ == "Hotspot"


def test_get_hotspots_succeeds(mocker, mock_hotspots) -> None:
    """It exits with a status code of zero."""
    mocker.patch(
        "helium_api_wrapper.hotspots.get_hotspots",
        return_value=[Hotspot(**hotspot) for hotspot in mock_hotspots],
        autospec=True,
    )

    result = hotspots.get_hotspots()
    assert type(result[0]).__name__ == "Hotspot"
    assert len(result) == 3


"""Test cases for ChallengeApi."""


def test_get_challenge_succeeds(mocker, mock_challenges) -> None:
    """It exits with a status code of zero."""
    mocker.patch(
        "helium_api_wrapper.challenges.get_challenges",
        return_value=[
            challenges.__resolve_challenge(Challenge(**challenge)) for challenge in mock_challenges
        ],
        autospec=True,
    )

    result = challenges.get_challenges(limit=5)
    assert type(result[0]).__name__ == "ChallengeResolved"
    assert len(result) == 5


"""Test cases for TransactionApi."""


def test_get_transactions_succeeds(mocker, mock_challenges) -> None:
    """It exits with a status code of zero."""
    mocker.patch(
        "helium_api_wrapper.challenges.get_challenge_by_id",
        return_value=challenges.__resolve_challenge(Challenge(**mock_challenges[0])),
        autospec=True,
    )
    result = challenges.get_challenge_by_id(
        id="0Q9A9Q0vpobgwy5zdq5EEgyrtQiiLSnZ9_ZxqdqWksQ"
    )
    assert type(result).__name__ == "ChallengeResolved"


"""Test cases for DeviceApi."""


def test_get_devices_succeeds(mocker, mock_devices) -> None:
    """It exits with a status code of zero."""
    mocker.patch(
        "helium_api_wrapper.devices.get_device_by_uuid",
        return_value=Device(**mock_devices[0]),
        autospec=True,
    )
    result = devices.get_device_by_uuid(uuid="some_uuid")
    assert type(result).__name__ == "Device"


def test_get_device_events(mocker, mock_events) -> None:
    """It exits with a status code of zero."""
    mocker.patch(
        "helium_api_wrapper.devices.get_events_for_device",
        return_value=[Event(**event) for event in mock_events],
        autospec=True,
    )
    result = devices.get_events_for_device(uuid="some_uuid")
    assert type(result[0]).__name__ == "Event"
    assert len(result) == 69


def test_get_device_last_event(mocker, mock_events) -> None:
    """It exits with a status code of zero."""
    mocker.patch(
        "helium_api_wrapper.devices.get_last_event",
        return_value=Event(**mock_events[0]),
        autospec=True,
    )
    result = devices.get_last_event(uuid="some_uuid")
    assert type(result).__name__ == "Event"


def test_get_device_integration(mocker, mock_integrations) -> None:
    """It exits with a status code of zero."""
    mocker.patch(
        "helium_api_wrapper.devices.get_last_integration",
        return_value=Event(**mock_integrations[0]),
        autospec=True,
    )
    result = devices.get_last_integration(uuid="some_uuid")
    assert type(result).__name__ == "Event"
    assert result.sub_category == "uplink_integration_req"
