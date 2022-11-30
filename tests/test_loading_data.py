"""Test cases for the helpers module."""
import pandas as pd
from numpy import int64

from helium_api_wrapper import helpers


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
    "hash": object,
    "time": int64,
    "distance": float,
}

address = "11BCGPgrFa2SxFMWfnv7S644uXX7jZTGmWVp3c2yhMh46G6pEbW"


def test_challenge_loading_triangulation() -> None:
    """Function testing if challenge data is loaded correctly."""
    test_df = pd.DataFrame(helpers.load_challenge_data(limit=1))

    # TESTING COLUMNS AND DATATYPES
    assert test_df.columns.tolist() == list(column_types.keys())
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

    # TESTING NUMBER OF WITNESSES
    # checking for doubles; key may not be reliable, as there may be duplicates,
    # if writing was stopped and then continued from the cursor
    assert (
        len(test_df[["challengee", "witness"]].drop_duplicates()) == 3
    ), "Wrong number of witnesses"

    # TESTING CHALLENGE VALIDITIES
    # checking, that none are False
    # assert test_df['valid'].value_counts()[True] == len(test_df)

    # TESTING FOR MAXIMUM DISTANCE
    # assert test_df['distance'].max() <= MAX_DISTANCE, "Distance too large"
