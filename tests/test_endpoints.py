"""Test cases for Endpoints."""
# import pytest

from helium_api_wrapper import challenges as challenges
from helium_api_wrapper import hotspots as hotspots


"""Test cases for HotspotApi."""


def test_get_hotspot_succeeds() -> None:
    """It exits with a status code of zero."""
    address = "11cxkqa2PjpJ9YgY9qK3Njn4uSFu6dyK9xV8XE4ahFSqN1YN2db"
    result = hotspots.get_hotspot_by_address(address)
    assert type(result[0]).__name__ == "Hotspot" or "str"


def test_get_hotspots_succeeds() -> None:
    """It exits with a status code of zero."""
    result = hotspots.get_hotspots(pages=1)
    assert type(result[0]).__name__ == "Hotspot" or "str"
    assert len(result) == 1000


def test_get_hotspot_roles_succeeds() -> None:
    """It exits with a status code of zero."""
    address = "11Jb4FjKJgPGvuejNDNEuGHvcWCqSJoSw98z4JizHnVPTFhfkVe"
    result = hotspots.load_roles(address, limit=2)
    if len(result) > 0:
        assert type(result[0]).__name__ == "Role"
        assert len(result) == 2


"""Test cases for ChallengeApi."""


def test_get_challenge_succeeds() -> None:
    """It exits with a status code of zero."""
    result = challenges.get_challenges(limit=5)
    assert type(result[0]).__name__ == "ChallengeResolved"
    assert len(result) == 5


"""Test cases for TransactionApi."""


def test_get_transactions_succeeds() -> None:
    """It exits with a status code of zero."""
    result = challenges.get_challenge_by_id(
        id="0Q9A9Q0vpobgwy5zdq5EEgyrtQiiLSnZ9_ZxqdqWksQ"
    )
    assert type(result).__name__ == "ChallengeResolved"
