"""Test cases data loading."""
import json
from typing import Any

import pandas as pd
import pytest
from numpy import int64
from pytest_mock import MockFixture

from helium_api_wrapper import challenges as challenges
from helium_api_wrapper.DataObjects import Challenge
from helium_api_wrapper.DataObjects import Hotspot


column_types = {
    "challengee": object,
    "challengee_lat": float,
    "challengee_lng": float,
    "witness": object,
    "witness_lat": float,
    "witness_lng": float,
    "signal": int64,
    "snr": float,
    "datarate": object,
    "is_valid": bool,
    "hash": object,
    "time": int64,
    "distance": float,
}


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


def test_challenge_loading_trilateration(
    mocker: MockFixture,
    mock_hotspots: Any,
    mock_challenges: Any,
) -> None:
    """Function testing if challenge data is loaded correctly."""
    mocker.patch(
        "helium_api_wrapper.hotspots.get_hotspot_by_address",
        return_value=Hotspot(**mock_hotspots[0]),
        autospec=True,
    )

    mocker.patch(
        "helium_api_wrapper.challenges.get_challenges",
        return_value=[challenges.__resolve_challenge(Challenge(**mock_challenges[0]))],
        autospec=True,
    )

    data = challenges.load_challenge_data(limit=1)
    test_df = pd.DataFrame([challenge.dict() for challenge in data])

    print(test_df.head())

    # TESTING COLUMNS AND DATATYPES
    # Following assertion is deactivated because we return everything, and don't filter it before.
    # assert test_df.columns.tolist() == list(column_types.keys())
    for key in column_types:
        assert key in test_df.columns, f"{key} is not a column"
        assert (
            test_df[key].dtype == column_types[key]
        ), f"{key} not of {column_types[key]}"

    # TESTING NUMBER OF CHALLENGEES
    # using both lat. and lon. on the off chance that two hotspots share one
    # but not both
    assert (
        len(test_df[["challengee"]].drop_duplicates()) == 1
    ), "Wrong number of challengees"
