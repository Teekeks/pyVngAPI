__all__ = ['OthersFleet', 'OthersShip', 'OthersShipMovement', 'OthersFuel', 'ShipLocation']

from dataclasses import dataclass
from datetime import datetime
from typing import List, Any, Dict, Literal

from mashumaro import DataClassDictMixin

from vng_api.types import Sector, Vector

type OthersShipType = Literal['mothership', 'standard'] | str


@dataclass
class OthersFuel(DataClassDictMixin):
    amount: float
    capacity: float


@dataclass
class ShipLocation(DataClassDictMixin):
    state: Literal['in_sector', 'transit', 'removed', 'destroyed'] | str


@dataclass
class OthersShipMovement(DataClassDictMixin):
    phase: Literal['waiting_to_depart', 'transit'] | str
    target: Vector
    """Destination relative to the owning player's home."""
    arrivalAt: datetime
    """Scheduled arrival date and time."""


@dataclass
class OthersShip(DataClassDictMixin):
    id: str
    fleetId: str
    type: OthersShipType
    status: str
    integrity: int
    maxIntegrity: int
    deuterium: OthersFuel
    inventoryCapacityEce: int
    location: ShipLocation
    sector: Sector
    movement: OthersShipMovement | None
    auxiliaryCount: int
    deployedAuxiliaryCount: int
    createdAt: datetime
    updatedAt: datetime


@dataclass
class OthersFleet(DataClassDictMixin):
    id: str
    status: str
    ships: List[OthersShip]
    activeActions: List[Dict[Any, Any]]
    createdAt: datetime
    updatedAt: datetime
