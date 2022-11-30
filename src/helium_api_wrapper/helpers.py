"""
.. module:: helpers

:synopsis: Functions to load data from Helium API

.. moduleauthor:: DSIA21

"""

import logging
from typing import Union

from haversine import haversine, Unit

from helium_api_wrapper import HotspotApi, ChallengeApi, TransactionApi, DeviceApi
from helium_api_wrapper.DataObjects import Hotspot

logging.basicConfig(level=logging.INFO)


def load_hotspots(page_amount: int = 1, filter_modes: str = "full"):
    """Load a list of hotspots.

    :param page_amount: Amount of pages to load
    :param filter_modes: Filter modes
    :return: List of hotspots
    """
    api = HotspotApi()
    hotspots = api.get_hotspots(page_amount=page_amount, filter_modes=filter_modes)
    return [
        hotspot.as_dict(["address", "location", "lat", "lng"]) for hotspot in hotspots
    ]


def load_roles(address: str, limit: int = 5, filter_types: str = "poc_receipts_v2"):
    """Load roles for a hotspot.

    :param address: Address of the hotspot
    :param limit: Limit of roles to load
    :param filter_types: Filter types for roles
    :return: List of roles
    """
    api = HotspotApi()
    roles = api.get_hotspot_roles(
        address=address, limit=limit, filter_types=filter_types
    )
    return [
        role.as_dict(["type", "role", "hash"])
        for role in roles
        if role.role == "challengee"
    ]


def load_challenge(hash: str):
    """Load a challenge.

    :param hash: Hash of the challenge
    :return: Challenge
    """
    api = TransactionApi()
    transaction = api.get_challenges_from_transactions(hash=hash)
    return transaction.as_dict(["hash", "witnesses", "time", "challengee"])


def load_challenges(limit: int = 50):
    """Load a list of challenges.

    :param limit: Limit of challenges to load
    :return: List of challenges
    """
    api = ChallengeApi()
    challenges = api.get_challenges(limit=limit)
    return [
        challenge.as_dict(["hash", "witnesses", "time", "challengee"])
        for challenge in challenges
    ]


def load_hotspot(address: str):
    """Load a hotspot.

    :param address: Address of the hotspot
    :return: Hotspot
    """
    api = HotspotApi()
    hotspot = api.get_hotspot_by_address(address=address)
    if isinstance(hotspot, Hotspot):
        return hotspot.as_dict(["address", "lat", "lng"])
    else:
        return None


def sort_witnesses(witnesses: list, load_type: str = "all"):
    """Sort witnesses by signal and limit by load type.

    :param witnesses: List of witnesses
    :param load_type: Load type
    :return: List of witnesses
    """
    # @todo: filter for valid witnesses
    if load_type == "all":
        return sorted(witnesses, key=lambda witness: witness["signal"], reverse=False)
    elif load_type == "triangulation":
        if len(witnesses) < 3:
            return sorted(
                witnesses, key=lambda witness: witness["signal"], reverse=False
            )
        return sorted(witnesses, key=lambda witness: witness["signal"], reverse=False)[
            :3
        ]
    elif load_type == "best_signal":
        if len(witnesses) == 0:
            return witnesses
        return sorted(witnesses, key=lambda witness: witness["signal"], reverse=False)[
            0
        ]
    else:
        return sorted(witnesses, key=lambda witness: witness["signal"], reverse=False)


# @todo: handle request timeouts
def load_challenges_for_hotspots(
    hotspots: list = None, load_type: str = "triangulation", limit: int = 50
):
    """Load challenges for hotspots.

    :param hotspots: List of hotspots
    :param load_type: Load type for witnesses
    :param limit: Limit of challenges to load
    :return: List of challenges
    """
    if hotspots is None:
        hotspots = load_hotspots()
    else:
        hotspots = hotspots
    for hotspot in hotspots:
        load_challenges_for_hotspot(hotspot, load_type=load_type, limit=limit)


def load_challenges_for_hotspot(
    hotspot: Union[list, str], load_type: str = "triangulation", limit: int = 5
):
    """Load challenges for a hotspot.

    :param hotspot: Hotspot
    :param load_type: Load type for witnesses
    :param limit: Limit of challenges to load
    :return: List of challenges
    """
    # Load hotspots
    if isinstance(hotspot, str):
        hotspot = load_hotspot(address=hotspot)
    else:
        hotspot = hotspot

    roles = load_roles(
        address=hotspot["address"], filter_types="poc_receipts_v2", limit=limit
    )
    for role in roles:
        # Load transaction
        challenge = load_challenge(hash=role["hash"])
        witnesses = sort_witnesses(challenge["witnesses"], load_type=load_type)
        for witness in witnesses:
            # Load witness
            witness_hotspot = load_hotspot(address=witness["address"])
            # Add to row
            yield get_challenge_data(
                challenge=challenge,
                witness=witness,
                witness_hotspot=witness_hotspot,
                challengee=hotspot,
            )


def load_challenge_data(
    challenges: list = None,
    load_type: str = "triangulation",
    limit: int = 50,
    load_hotspots: bool = True,
):
    """Load challenge data.

    :param challenges: List of challenges
    :param load_type: Load type for witnesses
    :param limit: Limit of challenges to load
    :return: List of challenges
    """
    if challenges is None:
        challenges = load_challenges(limit=limit)
    else:
        challenges = challenges

    for challenge in challenges:
        witnesses = sort_witnesses(challenge["witnesses"], load_type=load_type)
        if load_hotspots:
            challengee = load_hotspot(address=challenge["challengee"])
        else:
            challengee = {"address": challenge["challengee"], "lat": 0, "lng": 0}

        for witness in witnesses:
            if load_hotspots:
                witness_hotspot = load_hotspot(address=witness["gateway"])
            else:
                witness_hotspot = {"address": witness["gateway"], "lat": 0, "lng": 0}

            if witness_hotspot is None or challengee is None:
                return

            yield get_challenge_data(
                challenge=challenge,
                witness=witness,
                witness_hotspot=witness_hotspot,
                challengee=challengee,
            )


def get_challenge_data(challenge, witness, witness_hotspot, challengee):
    """Get challenge data.

    :param challenge: Challenge
    :param witness: Witness
    :param witness_hotspot: Witness hotspot
    :param challengee: Challengee
    :return: Challenge data
    """
    # @todo: check if best position for distance
    distance = haversine(
        (challengee["lat"], challengee["lng"]),
        (witness_hotspot["lat"], witness_hotspot["lng"]),
        unit=Unit.METERS,
    )
    return {
        "challengee": challengee["address"],
        "challengee_lat": challengee["lat"],
        "challengee_lng": challengee["lng"],
        "witness": witness_hotspot["address"],
        "witness_lat": witness_hotspot["lat"],
        "witness_lng": witness_hotspot["lng"],
        "signal": witness["signal"],
        "snr": witness["snr"],
        "datarate": witness["datarate"],
        "is_valid": witness["is_valid"],
        "hash": challenge["hash"],
        "time": challenge["time"],
        "distance": distance,
    }


def load_device(uuid: str):
    """Load a device.

    :param uuid: UUID of the device
    :return: Device
    """
    api = DeviceApi()
    return api.get_device(uuid=uuid)


def load_last_integration(uuid: str):
    """Load a device integration events.

    :param uuid: UUID of the device
    :return: Device
    """
    api = DeviceApi()
    integrations = api.get_integration_events(uuid=uuid)
    assert (
        len(integrations) > 0
    ), f"No Integration Events existing for device with uuid {uuid}"
    return integrations[0]


def load_last_event(uuid: str):
    """Load a device event.

    :param uuid: UUID of the device
    :return: Device
    """
    api = DeviceApi()
    integrations = api.get_events(uuid=uuid)
    assert len(integrations) > 0, f"No Events existing for device with uuid {uuid}"
    return integrations[0]
