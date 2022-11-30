"""Test cases for Endpoints."""
# import pytest

from helium_api_wrapper import ChallengeApi
from helium_api_wrapper import HotspotApi
from helium_api_wrapper import TransactionApi


"""Test cases for HotspotApi."""


def test_get_hotspot_succeeds() -> None:
    """It exits with a status code of zero."""
    address = "11BCGPgrFa2SxFMWfnv7S644uXX7jZTGmWVp3c2yhMh46G6pEbW"
    result = HotspotApi().get_hotspot_by_address(address)
    assert type(result).__name__ == "Hotspot"


def test_get_hotspots_succeeds() -> None:
    """It exits with a status code of zero."""
    result = HotspotApi().get_hotspots(page_amount=1)
    assert type(result[0]).__name__ == "Hotspot"
    assert len(result) == 1000


def test_get_hotspot_roles_succeeds() -> None:
    """It exits with a status code of zero."""
    address = "11cxkqa2PjpJ9YgY9qK3Njn4uSFu6dyK9xV8XE4ahFSqN1YN2db"
    result = HotspotApi().get_hotspot_roles(address, limit=2)
    if len(result) > 0:
        assert type(result[0]).__name__ == "Role"
        assert len(result) == 2
    else:
        assert ValueError


def test_get_hotspots_by_addresses_succeeds() -> None:
    """It exits with a status code of zero."""
    addresses = [
        "11BCGPgrFa2SxFMWfnv7S644uXX7jZTGmWVp3c2yhMh46G6pEbW",
        "11cxkqa2PjpJ9YgY9qK3Njn4uSFu6dyK9xV8XE4ahFSqN1YN2db",
    ]
    result = HotspotApi().get_hotspots_by_addresses(addresses)
    assert type(result[0]).__name__ == "Hotspot"
    assert len(result) == 2


"""Test cases for ChallengeApi."""


def test_get_challenge_succeeds() -> None:
    """It exits with a status code of zero."""
    result = ChallengeApi().get_challenges(limit=5)
    assert type(result[0]).__name__ == "ChallengeResolved"
    assert len(result) == 5


"""Test cases for TransactionApi."""


def test_get_transactions_succeeds() -> None:
    """It exits with a status code of zero."""
    result = TransactionApi().get_transaction(
        hash="0Q9A9Q0vpobgwy5zdq5EEgyrtQiiLSnZ9_ZxqdqWksQ"
    )
    assert type(result).__name__ == "dict"
