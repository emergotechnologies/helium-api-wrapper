"""
.. module:: __main__

:synopsis: Command-line interface

.. moduleauthor:: DSIA21

"""

# To start from cli:
# Install poetry then run the script defined in the pyproject.toml file under [tool.poetry.scripts]

# poetry install
# poetry run get-hotspot

import click

from helium_api_wrapper.ResultHandler import ResultHandler
from helium_api_wrapper.helpers import (
    load_hotspot,
    load_challenge_data,
    load_hotspots,
    load_device,
    load_challenges_for_hotspot,
    load_challenges,
    load_last_integration,
    load_last_event,
)


@click.command()
@click.option("--address", type=str, help="Address of the hotspot")
@click.option(
    "--file_format",
    default="pickle",
    type=str,
    help="Defines the format for the output file.",
)
@click.option(
    "--file_name", default="hotspot", type=str, help="Defines the name of the file."
)
@click.option(
    "--path", default="./data", type=str, help="Defines the path for the output file."
)
@click.version_option(version="0.1")
def get_hotspot(address: str, file_format: str, file_name: str, path: str):
    """
    This function returns a Hotspot for a given address.
    """
    if address:
        hotspot = load_hotspot(address)
    else:
        raise ValueError("No address given")

    ResultHandler(hotspot, file_format, file_name, path).write()


@click.command()
@click.option("--n", type=int, help="Nr. of pages to load. 1 page = 1000 hotspots")
@click.option(
    "--file_format",
    default="pickle",
    type=str,
    help="Defines the format for the output file.",
)
@click.option(
    "--file_name", default="hotspots", type=str, help="Defines the name of the file."
)
@click.option(
    "--path", default="./data", type=str, help="Defines the path for the output file."
)
@click.version_option(version="0.1")
def get_hotspots(n: int, file_format: str, file_name: str, path: str):
    """
    This function returns a the given number of random Hotspots.
    """
    hotspots = load_hotspots(n)
    ResultHandler(hotspots, file_format, file_name, path).write()


@click.command()
@click.option("--address", type=str, help="Address of the hotspot")
@click.option(
    "--file_format",
    default="pickle",
    type=str,
    help="Defines the format for the output file.",
)
@click.option(
    "--file_name", default="challenges", type=str, help="Defines the name of the file."
)
@click.option(
    "--path", default="./data", type=str, help="Defines the path for the output file."
)
@click.version_option(version="0.1")
def get_challenges_for_hotspot(
    address: str, file_format: str, file_name: str, path: str
):
    # print(f"called get_challenge with address {address}")
    ResultHandler(
        load_challenges_for_hotspot(address), file_format, file_name, path
    ).write()


@click.command()
@click.option("--n", type=int, help="Amount of challenges to return")
@click.option(
    "--incremental", is_flag=True, help="Set to save data after each challenge"
)
@click.option(
    "--file_format",
    default="pickle",
    type=str,
    help="Defines the format for the output file.",
)
@click.option(
    "--file_name", default="challenges", type=str, help="Defines the name of the file."
)
@click.option(
    "--path", default="./data", type=str, help="Defines the path for the output file."
)
@click.version_option(version="0.1")
def get_challenges(
    n: int, incremental: bool, file_format: str, file_name: str, path: str
):
    # print(f"called get_challenge_data")
    if incremental:
        result_hanlder = ResultHandler(None, file_format, file_name, path)
        challenges = load_challenges(limit=n)
        for challenge in challenges:
            result_hanlder.append(load_challenge_data([challenge]))
            result_hanlder.write()
    else:
        challenges = load_challenge_data(load_type="all", limit=n)
        ResultHandler(challenges, file_format, file_name, path).write()


@click.command()
@click.option("--uuid", type=str, help="UUID of the device")
@click.version_option(version="0.1")
def get_device(uuid: str):
    print(f"called get_device with uuid {uuid}")
    device = load_device(uuid)
    print(device)
    return device


@click.command()
@click.option("--uuid", type=str, help="UUID of the device")
@click.version_option(version="0.1")
def get_device_integration(uuid: str):
    # print(f"called get_device_integrations with uuid {uuid}")
    integration = load_last_integration(uuid)
    return integration


@click.command()
@click.option("--uuid", type=str, help="UUID of the device")
@click.version_option(version="0.1")
def get_device_event(uuid: str):
    # print(f"called get_device_event with uuid {uuid}")
    event = load_last_event(uuid)
    return event


@click.group(
    help="CLI tool to load data from the Helium Blockchain API and Helium Console API"
)
def cli():
    pass


cli.add_command(get_hotspot)
cli.add_command(get_hotspots)
cli.add_command(get_challenges)
cli.add_command(get_challenges_for_hotspot)
cli.add_command(get_device)
cli.add_command(get_device_integration)
cli.add_command(get_device_event)

if __name__ == "__main__":
    cli()
