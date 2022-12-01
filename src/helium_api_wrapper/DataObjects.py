"""Data Objects module.

.. module:: DataObjects

:synopsis: Classes for data from Helium API

.. moduleauthor:: DSIA21

"""

from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Union

from pydantic import BaseModel


class DataObject(BaseModel):
    """Base class for all data objects."""

    def __len__(self) -> int:
        return dict(self).__len__()

    def __getitem__(self, item) -> str:
        return getattr(self, item)

    def as_list(self, columns: Optional[List[str]] = None) -> List[Union[str, int]]:
        """Returns DataObject as List.

        :param columns: List of attributes to include
        :type columns: list

        :return: Dict of DataObject.
        :rtype: list
        """

        data = dict(self)
        if columns:
            data = {key: data[key] for key in columns}
        return data.values()

    def as_dict(self, columns: Optional[List[str]] = None) -> Dict[str, int]:
        """Returns DataObject as Dict.

        :param columns: List of attributes to include
        :type columns: list

        :return: Dict of DataObject.
        :rtype: dict
        """

        data = dict(self)
        if columns:
            data = {key: data[key] for key in columns}
        return data

    class Config:
        """Config Class for DataObject."""

        arbitrary_types_allowed = True


class Geocode(DataObject):
    """Class to describe Geocode Object."""

    long_city: Optional[str] = None
    long_country: Optional[str] = None
    long_state: Optional[str] = None
    long_street: Optional[str] = None
    short_city: Optional[str] = None
    short_country: Optional[str] = None
    short_state: Optional[str] = None
    short_street: Optional[str] = None
    city_id: Optional[str] = None


class Status(DataObject):
    """Class to describe Status Object."""

    height: Optional[int] = None
    online: Optional[str] = None


class Hotspot(DataObject):
    """Class to describe Hotspot Object."""

    address: Optional[str] = None
    block: Optional[int] = None
    block_added: Optional[int] = None
    geocode: Optional[Geocode] = None
    lat: Optional[float] = None
    lng: Optional[float] = None
    location: Optional[str] = None
    name: Optional[str] = None
    nonce: Optional[int] = None
    owner: Optional[str] = None
    reward_scale: Optional[float] = None
    status: Optional[Status] = None


class Role(DataObject):
    """Class to describe Role Object."""

    type: str
    time: int
    role: str
    height: Optional[int] = None
    hash: Optional[str] = None


class Witness(DataObject):
    """Class to describe Witness Object."""

    timestamp: int
    signal: int
    packet_hash: str
    owner: str
    location: str
    gateway: str
    is_valid: Optional[bool] = None
    datarate: Optional[str] = None
    snr: Optional[float] = None


class Receipt(DataObject):
    """Class to describe Receipt Object."""

    timestamp: int
    signal: int
    origin: str
    gateway: str
    data: str


class Challenge(DataObject):
    """Class to describe a Challenge loaded from the Helium API."""

    type: str
    time: int
    secret: str
    path: Optional[List[Dict[str, Any]]] = None
    onion_key_hash: Optional[str] = None
    height: Optional[int] = None
    hash: Optional[str] = None
    challenger_owner: Optional[str] = None
    challenger_lon: Optional[float] = None
    challenger_location: Optional[str] = None
    challenger_lat: Optional[float] = None
    challenger: Optional[str] = None
    fee: Optional[int] = None


class ChallengeResult(DataObject):
    """Class to describe a Challenge loaded from the Helium API."""

    challengee: Optional[str]
    challengee_lat: Optional[float]
    challengee_lng: Optional[float]
    witness_address: Optional[str]
    witness_lat: Optional[float]
    witness_lng: Optional[float]
    signal: Optional[int]
    snr: Optional[float]
    datarate: Optional[str]
    is_valid: Optional[bool]
    hash: Optional[str]
    time: Optional[int]
    distance: Optional[float]


class ChallengeResolved(DataObject):
    """Class to describe a resolved Challenge."""

    type: str
    time: int
    secret: str
    # path: List[Dict[str, AnyOptional[]]] = None
    onion_key_hash: Optional[str] = None
    height: Optional[int] = None
    hash: Optional[str] = None
    witnesses: Optional[List[Witness]] = None
    receipt: Optional[Receipt] = None
    geocode: Optional[Geocode] = None
    challengee_owner: Optional[str] = None
    challengee_lon: Optional[float] = None
    challengee_location: Optional[str] = None
    challengee_lat: Optional[float] = None
    challengee: Optional[str] = None
    challenger_owner: Optional[str] = None
    challenger_lon: Optional[float] = None
    challenger_location: Optional[str] = None
    challenger_lat: Optional[float] = None
    challenger: Optional[str] = None
    fee: Optional[int] = None


class Device(DataObject):
    """Class to describe Device in Helium API."""

    adr_allowed: Optional[bool] = None
    app_eui: Optional[str] = None
    app_key: Optional[str] = None
    cf_list_enabled: Optional[bool] = None
    dc_usage: Optional[int] = None
    dev_eui: Optional[str] = None
    id: Optional[str] = None
    in_xor_filter: Optional[bool] = None
    labels: Optional[List[str]] = None
    last_connected: Optional[str] = None
    name: Optional[str] = None
    organization_id: Optional[str] = None
    oui: Optional[str] = None
    total_packets: Optional[int] = None


class Event(DataObject):
    """Class to describe an Integration Event."""

    data: Dict[str, Any]
    description: str
    device_id: str
    frame_down: Optional[int] = None
    frame_up: Optional[int] = None
    organization_id: str
    reported_at: str
    router_uuid: str
    sub_category: str
