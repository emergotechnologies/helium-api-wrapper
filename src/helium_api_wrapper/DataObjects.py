"""
.. module:: DataObjects

:synopsis: Classes for data from Helium API

.. moduleauthor:: DSIA21

"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel


class DataObject(BaseModel):
    """Base class for all data objects."""

    def __len__(self):
        return dict(self).__len__()

    def __getitem__(self, item):
        return getattr(self, item)

    # TODO: I don't really think we need as_list and as_dict
    def as_list(self, columns: Optional[List[str]] = None):
        data = dict(self)
        if columns:
            data = {key: data[key] for key in columns}
        return data.values()

    def as_dict(self, columns: Optional[List[str]] = None):
        data = dict(self)
        if columns:
            data = {key: data[key] for key in columns}
        return data


class Geocode(DataObject):
    """Class to describe Geocode Object."""

    long_city: str = None
    long_country: str = None
    long_state: str = None
    long_street: str = None
    short_city: str = None
    short_country: str = None
    short_state: str = None
    short_street: str = None
    city_id: str = None


class Status(DataObject):
    """Class to describe Status Object."""

    height: int = None
    online: str = None


class Hotspot(DataObject):
    """Class to describe Hotspot Object."""

    address: str = None
    block: int = None
    block_added: int = None
    geocode: Geocode = None
    lat: float = None
    lng: float = None
    location: str = None
    name: str = None
    nonce: int = None
    owner: str = None
    reward_scale: float = None
    status: Status = None


class Role(DataObject):
    """Class to describe Role Object."""

    type: str
    time: int
    role: str
    height: int = None
    hash: str = None


class Witness(DataObject):
    """Class to describe Witness Object."""

    timestamp: int
    signal: int
    packet_hash: str
    owner: str
    location: str
    gateway: str
    is_valid: bool = None
    datarate: str = None
    snr: float = None


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
    path: List[Dict[str, Any]] = None
    onion_key_hash: str = None
    height: int = None
    hash: str = None
    challenger_owner: str = None
    challenger_lon: float = None
    challenger_location: str = None
    challenger_lat: float = None
    challenger: str = None
    fee: int = None


class ChallengeResolved(DataObject):
    """Class to describe a resolved Challenge"""

    type: str
    time: int
    secret: str
    # path: List[Dict[str, Any]] = None
    onion_key_hash: str = None
    height: int = None
    hash: str = None
    witnesses: List[Witness] = None
    receipt: Receipt = None
    geocode: Geocode = None
    challengee_owner: str = None
    challengee_lon: float = None
    challengee_location: str = None
    challengee_lat: float = None
    challengee: str = None
    challenger_owner: str = None
    challenger_lon: float = None
    challenger_location: str = None
    challenger_lat: float = None
    challenger: str = None
    fee: int = None


class Device(DataObject):
    """Class to describe Device in Helium API"""

    adr_allowed: bool = None
    app_eui: str = None
    app_key: str = None
    cf_list_enabled: bool = None
    dc_usage: int = None
    dev_eui: str = None
    id: str = None
    in_xor_filter: bool = None
    labels: List[str] = None
    last_connected: str = None
    name: str = None
    organization_id: str = None
    oui: str = None
    total_packets: int = None


class Event(DataObject):
    """Class to describe an Integration Event"""

    data: dict
    description: str
    device_id: str
    frame_down: int = None
    frame_up: int = None
    organization_id: str
    reported_at: str
    router_uuid: str
    sub_category: str
