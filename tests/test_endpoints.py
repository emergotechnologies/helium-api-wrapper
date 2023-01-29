"""Test cases for Endpoints."""
import json
from typing import Any

import pytest
from pytest_mock import MockFixture

from helium_api_wrapper import challenges as challenges
from helium_api_wrapper import devices as devices
from helium_api_wrapper import hotspots as hotspots
from helium_api_wrapper.DataObjects import Challenge
from helium_api_wrapper.DataObjects import Device
from helium_api_wrapper.DataObjects import Event
from helium_api_wrapper.DataObjects import Hotspot


@pytest.fixture
def mock_hotspots() -> Any:
    """Mock hotspots.

    :return: List of hotspots
    :rtype: Any
    """
    with open("tests/data/hotspots.json") as file:
        hotspot = json.load(file)
    return hotspot


@pytest.fixture
def mock_challenges() -> Any:
    """Mock challenges.

    :return: List of Challenges
    :rtype: Any
    """
    with open("tests/data/challenges.json") as file:
        challenge = json.load(file)
    return challenge


@pytest.fixture
def mock_devices() -> Any:
    """Mock devices.

    :return: List of devices
    :rtype: Any
    """
    with open("tests/data/devices.json") as file:
        device = json.load(file)
    return device


@pytest.fixture
def mock_integrations() -> Any:
    """Mock integrations.

    :return: List of integrations
    :rtype: Any
    """
    with open("tests/data/integration_events.json") as file:
        integration = json.load(file)
    return integration


@pytest.fixture
def mock_integrations_failed() -> Any:
    """Mock integrations.

    :return: List of integrations
    :rtype: Any
    """
    with open("tests/data/integration_events_failed.json") as file:
        integration = json.load(file)
    return integration


@pytest.fixture
def mock_events() -> Any:
    """Mock events.

    :return: List of events
    :rtype: Any
    """
    with open("tests/data/events.json") as file:
        event = json.load(file)
    return event


"""Test cases for HotspotApi."""


def test_get_hotspot_succeeds(mocker: MockFixture, mock_hotspots: Any) -> None:
    """It exits with a status code of zero."""
    mocker.patch(
        "helium_api_wrapper.hotspots.get_hotspot_by_address",
        return_value=Hotspot(**mock_hotspots[0]),
        autospec=True,
    )

    result = hotspots.get_hotspot_by_address(address="some_address")
    assert type(result).__name__ == "Hotspot"


def test_get_hotspots_succeeds(mocker: MockFixture, mock_hotspots: Any) -> None:
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


def test_get_challenge_succeeds(mocker: MockFixture, mock_challenges: Any) -> None:
    """It exits with a status code of zero."""
    mocker.patch(
        "helium_api_wrapper.challenges.get_challenges",
        return_value=[
            challenges.__resolve_challenge(Challenge(**challenge))
            for challenge in mock_challenges
        ],
        autospec=True,
    )

    result = challenges.get_challenges(limit=5)
    assert type(result[0]).__name__ == "ChallengeResolved"
    assert len(result) == 5


"""Test cases for TransactionApi."""


def test_get_transactions_succeeds(mocker: MockFixture, mock_challenges: Any) -> None:
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


def test_get_devices_succeeds(mocker: MockFixture, mock_devices: Any) -> None:
    """It exits with a status code of zero."""
    mocker.patch(
        "helium_api_wrapper.devices.get_device_by_uuid",
        return_value=Device(**mock_devices[0]),
        autospec=True,
    )
    result = devices.get_device_by_uuid(uuid="some_uuid")
    assert type(result).__name__ == "Device"


def test_get_device_events(mocker: MockFixture, mock_events: Any) -> None:
    """It exits with a status code of zero."""
    mocker.patch(
        "helium_api_wrapper.devices.get_events_for_device",
        return_value=[Event(**event) for event in mock_events],
        autospec=True,
    )
    result = devices.get_events_for_device(uuid="some_uuid")
    assert type(result[0]).__name__ == "Event"
    assert len(result) == 69


def test_get_device_last_event(mocker: MockFixture, mock_events: Any) -> None:
    """It exits with a status code of zero."""
    mocker.patch(
        "helium_api_wrapper.devices.get_last_event",
        return_value=Event(**mock_events[0]),
        autospec=True,
    )
    result = devices.get_last_event(uuid="some_uuid")
    assert type(result).__name__ == "Event"


def test_get_device_integration(mocker: MockFixture, mock_integrations: Any) -> None:
    """It exits with a status code of zero."""
    mocker.patch(
        "helium_api_wrapper.devices.get_last_integration",
        return_value=Event(**mock_integrations[0]),
        autospec=True,
    )
    result = devices.get_last_integration(uuid="some_uuid")

    assert type(result).__name__ == "Event"
    assert result.sub_category == "uplink_integration_req"


def test_get_device_integration_no_event(mocker: MockFixture, mock_integrations: Any) -> None:
    """It exits with a status code of zero."""
    mocker.patch(
        "helium_api_wrapper.devices.get_last_integration",
        return_value=Event(**mock_integrations_failed[0]),
        autospec=True,
    )
    with pytest.raises(Exception, match="No Integration Events existing for device with uuid some_uuid"):
        devices.get_last_integration(uuid="some_uuid")


def test_get_device_integration_no_hotspot(mocker: MockFixture, mock_integrations: Any) -> None:
    """It exits with a status code of zero."""
    mocker.patch(
        "helium_api_wrapper.devices.get_last_integration",
        return_value=Event(**mock_integrations[1]),
        autospec=True,
    )
    with pytest.raises(Exception, match="No Hotspots existing for integration of device with uuid some_uuid"):
        devices.get_last_integration(uuid="some_uuid")
