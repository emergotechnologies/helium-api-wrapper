"""Helpers Module.

.. module:: helpers

:synopsis: Functions to load data from Helium API

.. moduleauthor:: DSIA21

"""

import logging
from typing import Any
from typing import Dict
from typing import Generator
from typing import List
from typing import Optional

from haversine import Unit
from haversine import haversine

from helium_api_wrapper.ChallengeApi import ChallengeApi
from helium_api_wrapper.DataObjects import ChallengeResolved
from helium_api_wrapper.DataObjects import ChallengeResult
from helium_api_wrapper.DataObjects import Device
from helium_api_wrapper.DataObjects import Event
from helium_api_wrapper.DataObjects import Hotspot
from helium_api_wrapper.DataObjects import Role
from helium_api_wrapper.DataObjects import Witness
from helium_api_wrapper.DeviceApi import DeviceApi
from helium_api_wrapper.HotspotApi import HotspotApi
from helium_api_wrapper.TransactionApi import TransactionApi


logging.basicConfig(level=logging.INFO)


def load_hotspots(page_amount: int = 1, filter_modes: str = "full") -> List[Hotspot]:
    """Load a list of hotspots.

    :param page_amount: Amount of pages to load
    :param filter_modes: Filter modes
    :return: List of hotspots
    """
    api = HotspotApi()
    hotspots: List[Hotspot] = api.get_hotspots(
        page_amount=page_amount, filter_modes=filter_modes
    )
    return hotspots


def __load_roles(
    address: str, limit: int = 5, filter_types: str = "poc_receipts_v2"
) -> List[Role]:
    """Load roles for a hotspot.

    :param address: Address of the hotspot
    :param limit: Limit of roles to load
    :param filter_types: Filter types for roles
    :return: List of roles
    """
    api = HotspotApi()
    roles: List[Role] = api.get_hotspot_roles(
        address=address, limit=limit, filter_types=filter_types
    )
    return roles


def __load_challenge(hash: str) -> ChallengeResolved:
    """Load a challenge.

    :param hash: Hash of the challenge
    :return: Challenge
    """
    api = TransactionApi()
    return api.get_challenges_from_transactions(hash=hash)


def load_challenges(limit: int = 50) -> List[ChallengeResolved]:
    """Load a list of challenges.

    :param limit: Limit of challenges to load
    :return: List of challenges
    """
    api = ChallengeApi()
    challenges: List[ChallengeResolved] = api.get_challenges(limit=limit)
    return challenges


def load_hotspot(address: str) -> Optional[Hotspot]:
    """Load a hotspot.

    :param address: Address of the hotspot
    :return: Hotspot
    """
    api = HotspotApi()
    return api.get_hotspot_by_address(address=address)


def sort_witnesses(witnesses: List[Witness], load_type: str = "all") -> List[Witness]:
    """Sort witnesses by signal and limit by load type.

    :param witnesses: List of witnesses
    :param load_type: Load type
    :return: List of witnesses
    """
    return_witnesses: List[Witness]
    if load_type == "triangulation":
        return_witnesses = sorted(
            witnesses, key=lambda witness: witness.signal, reverse=False  # type: ignore
        )[: max(3, len(witnesses))]
    elif load_type == "best_signal":
        if len(witnesses) == 0:
            return witnesses
        return_witnesses = [
            sorted(
                witnesses, key=lambda witness: witness.signal, reverse=False  # type: ignore
            )[0]
        ]
    else:
        return_witnesses = sorted(
            witnesses,
            key=lambda witness: witness.signal,  # type: ignore
            reverse=False,
        )
    return return_witnesses


# @todo: handle request timeouts
def load_challenges_for_hotspots(
    hotspots: Optional[Hotspot] = None,
    load_type: str = "triangulation",
    limit: int = 50,
) -> None:
    """Load challenges for hotspots.

    :param hotspots: List of hotspots
    :param load_type: Load type for witnesses
    :param limit: Limit of challenges to load
    :return: List of challenges
    """
    if hotspots is None:
        hotspots = load_hotspots()

    for hotspot in hotspots:
        load_challenges_for_hotspot(hotspot.address, load_type=load_type, limit=limit)


def load_challenges_for_hotspot(
    hotspot_address: str, load_type: str = "triangulation", limit: int = 5
) -> Generator[Optional[Dict[str, Any]], None, None]:
    """Load challenges for a hotspot.

    :param hotspot: Hotspot
    :param load_type: Load type for witnesses
    :param limit: Limit of challenges to load
    :return: List of challenges
    """
    hotspot = load_hotspot(address=hotspot_address)
    if hotspot is None or hotspot.address is None:
        yield None
    else:
        roles = __load_roles(
            address=hotspot.address or "", filter_types="poc_receipts_v2", limit=limit
        )
        for role in roles:
            # Load transaction
            challenge = __load_challenge(hash=role.hash)
            witnesses = sort_witnesses(challenge.witnesses, load_type=load_type)
            for witness in witnesses:
                # Load witness
                witness_hotspot = load_hotspot(address=witness.gateway)
                # Add to row
                yield __get_challenge_data(
                    challenge=challenge,
                    witness=witness,
                    hotspot=witness_hotspot,
                    challengee=hotspot,
                )


def load_challenge_data(
    challenges: Optional[List[ChallengeResolved]] = None,
    load_type: str = "triangulation",
    limit: int = 50,
) -> Generator[Dict[str, Any], None, None]:
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
        witnesses = sort_witnesses(challenge.witnesses, load_type=load_type)
        challengee = load_hotspot(address=challenge.challengee)

        for witness in witnesses:
            witness_hotspot = load_hotspot(address=witness.gateway)

            if witness_hotspot is None or challengee is None:
                return

            yield __get_challenge_data(
                challenge=challenge,
                witness=witness,
                hotspot=witness_hotspot,
                challengee=challengee,
            )


def __get_challenge_data(  # TODO: check if this works I did a lot of changes here I might have messed stuff up
    challenge: ChallengeResolved,
    witness: Witness,
    hotspot: Hotspot,
    challengee: Hotspot,
) -> ChallengeResult:
    """Get challenge data.

    :param challenge: Challenge
    :param witness: Witness
    :param hotspot: Witness hotspot
    :param challengee: Challengee
    :return: Challenge data
    """
    # @todo: check if best position for distance
    distance = haversine(
        (challengee.lat, challengee.lng),
        (hotspot.lat, hotspot.lng),
        unit=Unit.METERS,
    )
    return ChallengeResult(
        challengee=challengee.address,
        challengee_lat=challengee.lat,
        challengee_lng=challengee.lng,
        witness=hotspot.address,
        witness_lat=hotspot.lat,
        witness_lng=hotspot.lng,
        signal=witness.signal,
        snr=witness.snr,
        datarate=witness.datarate,
        is_valid=witness.is_valid,
        hash=challenge.hash,
        time=challenge.time,
        distance=distance,
    )


def load_device(uuid: str) -> Device:
    """Load a device.

    :param uuid: UUID of the device
    :return: Device
    """
    api = DeviceApi()
    return api.get_device(uuid=uuid)


def load_last_integration(uuid: str) -> Event:
    """Load a device integration events.

    :param uuid: UUID of the device
    :return: Device
    """
    api = DeviceApi()
    integrations = api.get_integration_events(uuid=uuid)
    if len(integrations) > 0:
        print(f"No Integration Events existing for device with uuid {uuid}")
    return integrations[0]


def load_last_event(uuid: str) -> Event:
    """Load a device event.

    :param uuid: UUID of the device
    :return: Device
    """
    api = DeviceApi()
    integrations = api.get_events(uuid=uuid)
    if len(integrations) > 0:
        print(f"No Events existing for device with uuid {uuid}")
    return integrations[0]
