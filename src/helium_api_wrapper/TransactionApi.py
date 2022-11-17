"""
.. module:: TransactionApi

:synopsis: Functions to load the transaction data from Helium API

.. moduleauthor:: DSIA21

"""

import logging
from typing import Union

from helium_api_wrapper.Endpoint import Endpoint
from helium_api_wrapper.DataObjects import DataObject, ChallengeResolved

logging.basicConfig(level=logging.INFO)


class TransactionApi:
    """Class to describe Transaction API
    """
    def __init__(self, logger: logging.Logger = None):
        if logger is None:
            self.logger = logging.getLogger(__name__)
        else:
            self.logger = logger

    # @todo: move to Endpoint.py
    def get_endpoint(self, endpoint_url="transactions", params=None, response: DataObject = None) -> Endpoint:
        """Load the hotspot data.


        :param endpoint_url: The url of the endpoint, defaults to "hotspots"
        :type: str, optional

        :param params: The parameters to send with the request, defaluts to {}
        :type: dict, optional

        :param response: The type of the data, defaults to None
        :type: DataObject, optional

        :return: The endpoint.
        :rtype: Endpoint
        """
        if params is None:
            params = {}
        endpoint = Endpoint(endpoint_url, "GET", params, response_type=response)
        return endpoint

    def get_transaction(self, hash: str) -> dict:
        """Get a hotspot by address.

        :param hash: The hash of the transaction, defaults to None
        :type: str

        :return: The transaction.
        :rtype: Transaction
        """
        self.logger.info(f"Getting transaction for hash {hash}")
        endpoint = self.get_endpoint(f"transactions/{hash}")
        endpoint.request_with_exponential_backoff()
        return endpoint.data[0]

    def get_challenges_from_transactions(self, hash: str) -> Union[ChallengeResolved, dict]:
        """Get a hotspot by address.

        :param hash: The hash of the transaction, defaults to None
        :type: str

        :return: The resolved challenge or raw data.
        :rtype: ChallengeResolved, dict
        """
        self.logger.info(f"Getting challenges from transaction {hash}")
        challenge = self.get_transaction(hash)
        print(challenge)
        if challenge['type'] == 'poc_receipts_v2':
            challenge_resolved = {key: challenge[key] for key in challenge if key != 'path'}
            challenge_resolved.update(challenge['path'][0])
            return ChallengeResolved(**challenge_resolved)
        else:
            self.logger.info(f"Transaction {hash} is not a challenge. Returning Data")
            return challenge
