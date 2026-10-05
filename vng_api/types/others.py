__all__ = ['OthersFleet', 'OthersShip', 'OthersShipMovement', 'OthersFuel', 'ShipLocation', 'OthersFleetSummary', 'OthersFleetMoveResponse',
           'ActionActor', 'MoveAction', 'BlockedMove', 'IgnoredMove', 'OthersFleetMoveAcceptedAction', 'OthersDepotSummary',
           'OthersPlanetHarvestAction', 'OthersCraft', 'OthersCraftResult', 'OthersCraftResultOutput', 'OthersCraftAction', 'OthersCraftResponse',
           'OthersLaserLockAction', 'OthersMissileLaunchResponse', 'OthersMissileLaunchAction', 'OthersAuxiliariesResponse', 'OthersAuxiliary',
           'OthersDepotContent', 'OthersDepotActionBase', 'OthersError', 'OthersDepotTransferAction', 'OthersDepotTransferResult',
           'OthersDepotTransfer', 'OthersResourceAmounts', 'OthersResourceAmount', 'OthersInventoryItem', 'OthersShipInventory',
           'OthersInventoryTransferCreateResponse', 'OthersInventoryTransfer', 'OthersInventoryTransferAction', 'OthersTransferResult',
           'OthersInventoryResourceJettisonResult', 'OthersInventoryItemJettisonResult', 'OthersInventoryJettisonResult',
           'OthersInventoryJettisonResponse', 'OthersScan', 'OthersObservedProbe', 'OthersSectorObservation', 'OthersObservedSectorObject',
           'OthersObjectMovement', 'OthersScanSource']

from dataclasses import dataclass
from datetime import datetime
from typing import List, Any, Dict, Literal

from mashumaro import DataClassDictMixin
from mashumaro.config import BaseConfig
from mashumaro.types import Discriminator

from vng_api.types import Sector, Vector, MissileState, ResourceAmounts, ResourceType, AutonomousUnitCarrier

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
    createdAt: datetime
    updatedAt: datetime
    auxiliaryCount: int | None = None
    deployedAuxiliaryCount: int | None = None


@dataclass
class OthersFleet(DataClassDictMixin):
    id: str
    status: str
    ships: List[OthersShip]
    activeActions: List[Dict[Any, Any]]
    createdAt: datetime
    updatedAt: datetime


@dataclass
class OthersFleetSummary(DataClassDictMixin):
    id: str
    status: str
    shipCount: int
    standardShipCount: int
    auxiliaryCount: int
    deployedAuxiliaryCount: int
    activeActionCount: int


@dataclass
class ActionActor(DataClassDictMixin):
    kind: str
    id: str


@dataclass
class OthersFleetMoveAcceptedAction(DataClassDictMixin):
    id: str
    """Public action identifier for GET /api/others/actions/{actionId}."""
    type: Literal['ship_move'] | str
    status: Literal['queued'] | str
    actor: ActionActor
    createdAt: datetime
    updatedAt: datetime
    endsAt: datetime
    """Scheduled arrival time, including the departure preparation period."""
    cancelableUntil: datetime
    """End of the fifteen-minute cancellation window; scheduled departure time."""


@dataclass
class MoveAction(DataClassDictMixin):
    shipId: str
    action: OthersFleetMoveAcceptedAction


@dataclass
class IgnoredMove(DataClassDictMixin):
    shipId: str
    reason: str


@dataclass
class BlockedMove(DataClassDictMixin):
    shipId: str
    reason: str


@dataclass
class OthersFleetMoveResponse(DataClassDictMixin):
    actions: List[MoveAction]
    """Successfully scheduled moves; empty when no ship can start a move."""
    ignored: List[IgnoredMove]
    """Ships already in the requested sector; no action is created for them."""
    blocked: List[BlockedMove]
    """Ships whose individual move was refused. No action is created for these entries. Each entry contains a reason code, not an error object
    or a human-readable message."""


@dataclass
class OthersDepotSummary(DataClassDictMixin):
    relativeCoordinates: Vector


@dataclass
class OthersPlanetHarvestAction(DataClassDictMixin):
    id: str
    type: Literal['planet_harvest']
    status: Literal['queued'] | str
    createdAt: datetime
    updatedAt: datetime
    actor: ActionActor
    endsAt: datetime


@dataclass
class OthersCraftResultOutput(DataClassDictMixin):
    kind: str
    id: str


@dataclass
class OthersCraftResult(DataClassDictMixin):
    output: OthersCraftResultOutput


@dataclass
class OthersCraft(DataClassDictMixin):
    id: str
    recipeId: str
    status: str
    actionId: str
    createdAt: datetime
    updatedAt: datetime
    endsAt: datetime
    result: OthersCraftResult | None = None


@dataclass
class OthersCraftAction(DataClassDictMixin):
    id: str
    type: Literal['others_craft']
    status: str
    createdAt: datetime
    updatedAt: datetime
    actor: ActionActor
    endsAt: datetime


@dataclass
class OthersCraftResponse(DataClassDictMixin):
    craft: OthersCraft
    action: OthersCraftAction


@dataclass
class OthersLaserLockAction(DataClassDictMixin):
    id: str
    type: Literal['laser_lock']
    status: str
    createdAt: datetime
    updatedAt: datetime
    actor: ActionActor


@dataclass
class OthersMissileLaunchAction(DataClassDictMixin):
    id: str
    type: Literal['missile_launch']
    status: str
    createdAt: datetime
    updatedAt: datetime
    actor: ActionActor


@dataclass
class OthersMissileLaunchResponse(DataClassDictMixin):
    missile: MissileState
    action: OthersMissileLaunchAction


@dataclass
class OthersAuxiliary(DataClassDictMixin):
    id: str
    status: str
    locationType: str
    spatialState: str
    capacityEce: float
    cargo: ResourceAmounts
    sector: Sector | None = None
    """Present only when the auxiliary is separated from its carrier, or while its carrier is in transit. 
    Coordinates are relative to the owning player's home."""
    action: Dict[Any, Any] | None = None


@dataclass
class OthersAuxiliariesResponse(DataClassDictMixin):
    auxiliaries: List[OthersAuxiliary]
    nextCursor: str | None = None


@dataclass
class OthersError(DataClassDictMixin):
    code: str
    message: str


@dataclass
class OthersDepotActionBase(DataClassDictMixin):
    id: str
    """Opaque action id retained after the auxiliary disappears."""
    type: Literal['build_germination_depot', 'depot_deposit', 'depot_withdrawal'] | str
    status: Literal['queued', 'succeeded', 'failed', 'canceled'] | str
    """queued until terminal settlement; succeeded on completion, canceled on carrier departure/destruction, failed on auxiliary destruction. 
    Completion already due at interruption takes precedence."""
    actor: ActionActor
    createdAt: datetime
    updatedAt: datetime
    endsAt: datetime
    """Scheduled deadline; retained even when interrupted earlier."""
    completedAt: datetime | None = None
    """Present after terminal settlement; omitted while queued."""
    error: OthersError | None = None
    """Present only when an error was recorded. An interruption can have a result without error."""


@dataclass
class OthersDepotTransfer(DataClassDictMixin):
    depotId: str
    resources: ResourceAmounts
    itemIds: List[str]
    capacityEce: float
    roundTrips: int
    """Number of actual indivisible loads; not just total volume divided by capacity."""
    durationSeconds: int
    """roundTrips multiplied by 600 seconds (300 outbound and 300 returning)."""


@dataclass
class OthersDepotContent(DataClassDictMixin):
    resources: ResourceAmounts
    itemIds: List[str]


@dataclass
class OthersDepotTransferResult(DataClassDictMixin):
    outcome: Literal['delivered', 'carrier_departure', 'carrier_destroyed', 'auxiliary_destroyed'] | str
    delivered: OthersDepotContent
    """Content credited to destination. Includes the whole outgoing deposit on carrier departure/destruction; 
    interrupted withdrawals deliver nothing."""
    lost: OthersDepotContent
    """Only the virtual load carried when the auxiliary was destroyed. An empty leg loses nothing; 
    earlier virtual trips are not credited separately."""
    released: OthersDepotContent
    """Content left at its source and unreserved, without crediting it again."""
    dormantAuxiliaryId: str | None = None
    """Present on carrier_departure or carrier_destroyed; public sector-object id of the intact dormant auxiliary. 
    Absent on success or auxiliary destruction."""


@dataclass
class OthersDepotTransferAction(OthersDepotActionBase, DataClassDictMixin):
    transfer: OthersDepotTransfer | None = None
    result: OthersDepotTransferResult | None = None


@dataclass
class OthersResourceAmount(DataClassDictMixin):
    amount: float
    reserved: float


@dataclass
class OthersResourceAmounts(DataClassDictMixin):
    deuterium: OthersResourceAmount
    metals: OthersResourceAmount
    ice: OthersResourceAmount
    carbon_compounds: OthersResourceAmount


@dataclass
class OthersInventoryItem(DataClassDictMixin):
    id: str
    type: str
    containerSpaceEce: float


@dataclass
class OthersShipInventory(DataClassDictMixin):
    shipId: str
    capacityEce: float
    usedEce: float
    reservedEce: float
    resources: OthersResourceAmounts
    items: List[OthersInventoryItem]


@dataclass
class OthersTransferResult(DataClassDictMixin):
    outcome: Literal['transferred'] | str


@dataclass
class OthersInventoryTransfer(DataClassDictMixin):
    id: str
    kind: str
    status: str
    actionId: str
    endsAt: datetime
    result: OthersTransferResult | None = None
    error: OthersError | None = None
    resourceType: ResourceType | None = None
    amount: float | None = None
    itemIds: List[str] | None = None


@dataclass
class OthersInventoryTransferAction(DataClassDictMixin):
    id: str
    type: Literal['inventory_transfer'] | str
    status: Literal['queued', 'succeeded', 'failed'] | str
    actor: ActionActor
    createdAt: datetime
    updatedAt: datetime
    endsAt: datetime
    completedAt: datetime | None = None
    result: Dict[Any, Any] | None = None
    error: Dict[Any, Any] | None = None


@dataclass
class OthersInventoryTransferCreateResponse(DataClassDictMixin):
    transfer: OthersInventoryTransfer
    action: OthersInventoryTransferAction


@dataclass
class OthersInventoryJettisonResult:
    class Config(BaseConfig):
        discriminator = Discriminator(field='kind', include_subtypes=True)


@dataclass
class OthersInventoryResourceJettisonResult(OthersInventoryJettisonResult, DataClassDictMixin):
    kind: Literal['resource']
    resourceType: ResourceType
    amount: float


@dataclass
class OthersInventoryItemJettisonResult(OthersInventoryJettisonResult, DataClassDictMixin):
    kind: Literal['item']
    itemId: str
    type: str
    objectId: str
    driftingQuantity: int
    containerSpaceEce: float


@dataclass
class OthersInventoryJettisonResponse(DataClassDictMixin):
    jettisoned: OthersInventoryJettisonResult
    inventory: OthersShipInventory


@dataclass
class OthersObjectMovement(DataClassDictMixin):
    direction: Vector


@dataclass
class OthersObservedSectorObject(DataClassDictMixin):
    id: str | int | None = None
    type: str | None = None
    observedClass: str | None = None
    """Present on dynamically observed ships and projectiles."""
    status: str | None = None
    """Current status of a dynamically observed ship."""
    estimated: bool | None = None
    harvestable: bool | None = None
    """Present only on planets observed locally by an Others fleet ship, including planet entries nested in bookmarkTargets and minableTargets. 
    True when remaining planetary resources total strictly more than 5 ECE."""
    movement: OthersObjectMovement | None = None


@dataclass
class OthersObservedProbe(DataClassDictMixin):
    id: int
    name: str
    status: Literal['idle', 'preparing', 'accelerating', 'cruising', 'decelerating', 'orbiting', 'disabled', 'trapped_by_black_hole', 'dead'] | str


@dataclass
class OthersScanSource(DataClassDictMixin):
    id: str
    kind: Literal['others_ship'] | str


@dataclass
class OthersScan(DataClassDictMixin):
    currentSectorResidenceSeconds: int
    requiredResidenceSeconds: int
    scanQuality: int
    source: OthersScanSource


@dataclass
class OthersSectorObservation(DataClassDictMixin):
    relativeCoordinates: Vector
    distance: int
    """Distance from the closest active ship in the designated fleet."""
    knowledgeLevel: Literal['detailed', 'neighbor_scan', 'distant_scan', 'long_range_estimation'] | str
    confidence: float
    scan: OthersScan
    objects: List[OthersObservedSectorObject] | None = None
    """Detailed natural sector content and observable moving projectiles. Detected ship entries are included only when a ship of the designated 
    fleet is physically present in this sector."""
    probes: List[OthersObservedProbe] | None = None
    """Probes physically observable in the sector and their live status. Present, possibly empty, only when a ship of the designated fleet is 
    physically present in the requested sector."""
    estimatedObjects: Dict[Any, Any] | None = None
    possibleObjects: List[str] | None = None
    navigationalRisk: str | None = None
    message: str | None = None
