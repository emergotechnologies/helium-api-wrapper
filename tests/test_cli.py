"""Test cases for the __main__ module."""
import pytest
from click.testing import CliRunner

from helium_api_wrapper.__main__ import get_hotspot
from helium_api_wrapper.__main__ import load_hotspots


@pytest.fixture
def runner() -> CliRunner:
    """Fixture for invoking command-line interfaces."""
    return CliRunner()


def c_get_hotspot(runner: CliRunner) -> None:
    """It exits with a status code of zero."""
    result = runner.invoke(
        get_hotspot,
        ["--address", "11BCGPgrFa2SxFMWfnv7S644uXX7jZTGmWVp3c2yhMh46G6pEbW"],
    )
    assert result.exit_code == 0


def c_load_hotspots(runner: CliRunner) -> None:
    """It exits with a status code of zero."""
    result = runner.invoke(
        load_hotspots,
        ["--n", 1],
    )
    assert result.exit_code == 0
