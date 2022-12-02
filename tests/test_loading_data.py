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
    "is_valid": bool,
    "hash": object,
    "time": int64,
    "distance": float,
}


def test_challenge_loading_triangulation() -> None:
    """Function testing if challenge data is loaded correctly."""
    challenges = helpers.load_challenge_data(limit=1)
    test_df = pd.DataFrame([challenge.dict() for challenge in challenges])

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
