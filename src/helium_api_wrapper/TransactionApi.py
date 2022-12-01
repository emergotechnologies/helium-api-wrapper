"""TranscriptionApi module.

.. module:: TransactionApi

:synopsis: Functions to load the transaction data from Helium API

.. moduleauthor:: DSIA21

"""

import logging
from typing import Dict
from typing import Optional
from typing import Union

from helium_api_wrapper.DataObjects import ChallengeResolved
from helium_api_wrapper.DataObjects import DataObject
from helium_api_wrapper.Endpoint import Endpoint


logging.basicConfig(level=logging.INFO)


class TransactionApi:
    """Class to describe Transaction API."""

    def __init__(self, logger: Optional[logging.Logger] = None):
        self.logger: logging.Logger = logger or logging.getLogger(__name__)

    def get_endpoint(
        self,
        endpoint_url: str = "transactions",
        params: Optional[Dict[str, Union[str, int]]] = None,
        response: DataObject = None,
    ) -> Endpoint:
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
        endpoint = Endpoint(
            name=endpoint_url, method="GET", params=params, response_type=response
        )
        return endpoint

    def get_transaction(self, hash: str) -> DataObject:
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

    def get_challenges_from_transactions(
        self, hash: str
    ) -> ChallengeResolved:  # TODO: check if this really returns a Dict
        """Get a hotspot by address.

        :param hash: The hash of the transaction, defaults to None
        :type: str

        :return: The resolved challenge or raw data.
        :rtype: ChallengeResolved, dict
        """
        self.logger.info(f"Getting challenges from transaction {hash}")
        challenge = self.get_transaction(hash)
        self.logger.info(challenge)
        if challenge["type"] == "poc_receipts_v2":
            # flatten the data, this is dangerous we should look over this
            challenge_resolved = {
                key: value for key, value in challenge if key != "path"
            }
            challenge_resolved.update(challenge["path"][0])
            return ChallengeResolved(**challenge_resolved)
        else:
            self.logger.info(f"Transaction {hash} is not a challenge. Returning Data")
            return None  # TODO: should we return none or why do we only use poc_receipts_v2?
