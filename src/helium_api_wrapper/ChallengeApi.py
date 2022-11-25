"""
.. module:: ChallengeApi

:synopsis: Functions to load challenges from Helium API

.. moduleauthor:: DSIA21

"""

import logging
from dataclasses import asdict
from typing import List

from helium_api_wrapper.Endpoint import Endpoint
from helium_api_wrapper.DataObjects import Challenge, ChallengeResolved, DataObject

logging.basicConfig(level=logging.INFO)


class ChallengeApi:
    """Class to describe Challenge API
    """
    def __init__(self, logger: logging.Logger = None):
        if logger is None:
            self.logger = logging.getLogger(__name__)
        else:
            self.logger = logger

    def get_endpoint(self, endpoint_url="challenges", params=None, response: DataObject = Challenge) -> Endpoint:
        """Load the hotspot data.


        :param endpoint_url: The url of the endpoint, defaults to "challenges"
        :type endpoint_url: str, optional

        :param params: The parameters to send with the request, defaults to {}
        :type params: dict, optional

        :param response: The type of the data, defaults to Challenge
        :type response: DataObject, optional

        :return: The endpoint.
        :rtype: Endpoint
        """
        if params is None:
            params = {}
        endpoint = Endpoint(endpoint_url, "GET", params, response_type=response)
        return endpoint

    def get_challenges(self, address: str = "", limit: int = 50) -> List[ChallengeResolved]:
        """Get a list of challenges.
        When passed an address, it will get the challenges for that hotspot.

        :param address: The address of the hotspot, defaults to ""
        :type address: str, optional

        :param limit: The amount of challenges to get. Defaults to 50
        :type limit: int

        :return: The challenges.
        :rtype: list[Challenge]
        """
        if address != "":
            self.logger.info(f"Getting challenges for {address}")
            endpoint = self.get_endpoint(
                f"hotspots/{address}/challenges", response=Challenge,
                params={"limit": limit}
            )
        else:
            self.logger.info(f"Getting challenges")
            endpoint = self.get_endpoint(
                "challenges", response=Challenge,
                params={"limit": limit}
            )

        endpoint.crawl_pages(page_amount=10)

        challenges = []
        for challenge in endpoint.data:
            challenges.append(self.resolve_challenge(challenge))
        return challenges

    def resolve_challenge(self, challenge: Challenge) -> ChallengeResolved:
        """Resolve a challenge.

        :param challenge: The challenge to resolve, defaults to None
        :type: Challenge

        :return: The resolved challenge.
        :rtype: ChallengeResolved
        """
        self.logger.info(f"Resolving challenge {challenge.hash}")
        challenge = challenge.as_dict()

        # We can assume the path to be length 0 or 1 because Multihop PoC is deprecated.
        # see https://github.com/helium/HIP/blob/main/0015-beaconing-rewards.md
        challenge_resolved = {key: challenge[key] for key in challenge if key != 'path'}
        challenge_resolved.update(challenge['path'][0])
        return ChallengeResolved(**challenge_resolved)
