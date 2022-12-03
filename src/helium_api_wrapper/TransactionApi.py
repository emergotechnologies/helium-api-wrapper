"""TranscriptionApi module.

.. module:: TransactionApi

:synopsis: Functions to load the transaction data from Helium API

.. moduleauthor:: DSIA21

"""

import logging
from typing import Dict
from typing import Optional
from typing import Union

from pydantic import BaseModel

from helium_api_wrapper.DataObjects import ChallengeResolved
from helium_api_wrapper.Endpoint import Endpoint


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TransactionApi:
    """Class to describe Transaction API."""

    def get_endpoint(
        self,
        endpoint_url: str = "transactions",
        params: Optional[Dict[str, Union[str, int]]] = None,
        response: BaseModel = BaseModel,
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
        endpoint = Endpoint(url=endpoint_url, params=params, response_type=response)
        return endpoint

    def get_transaction(self, hash: str) -> BaseModel:
        """Get a hotspot by address.

        :param hash: The hash of the transaction, defaults to None
        :type: str

        :return: The transaction.
        :rtype: Transaction
        """
        logger.info(f"Getting transaction for hash {hash}")
        endpoint = self.get_endpoint(f"transactions/{hash}")
        endpoint.request_with_exponential_backoff()
        return endpoint.data[0]

    def get_challenges_from_transactions(self, hash: str) -> ChallengeResolved:
        """Get a hotspot by address.

        :param hash: The hash of the transaction, defaults to None
        :type: str

        :return: The resolved challenge or raw data.
        :rtype: ChallengeResolved, dict
        """
        logger.info(f"Getting challenges from transaction {hash}")
        challenge = self.get_transaction(hash)
        logger.info(challenge)
        if challenge["type"] == "poc_receipts_v2":
            # flatten the data, this is dangerous we should look over this
            challenge_resolved = {
                key: value for key, value in challenge if key != "path"
            }
            challenge_resolved.update(challenge["path"][0])
            return ChallengeResolved(**challenge_resolved)
        else:
            logger.info(f"Transaction {hash} is not a challenge. Returning Data")
            return None  # TODO: should we return none or why do we only use poc_receipts_v2?
