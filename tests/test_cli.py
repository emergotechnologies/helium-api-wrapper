"""Test cases for the __main__ module."""
import pytest
from click.testing import CliRunner

from helium_api_wrapper.__main__ import get_hotspot


@pytest.fixture
def runner() -> CliRunner:
    """Fixture for invoking command-line interfaces."""
    return CliRunner()


def test_main_succeeds(runner: CliRunner) -> None:
    """It exits with a status code of zero."""
    result = runner.invoke(
        get_hotspot,
        ["--address", "11BCGPgrFa2SxFMWfnv7S644uXX7jZTGmWVp3c2yhMh46G6pEbW"],
    )
    assert result.exit_code == 0
