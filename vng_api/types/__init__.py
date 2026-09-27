__all__ = ['Vector', 'Sector', 'SectorVisitHistory', 'SectorObservation', 'SectorScan', 'SectorObject', 'BookmarkableSectorObject',
           'WaypointBookmark', 'ResourceAmounts', 'ScutRelay', 'ScutNetwork', 'MineableSectorObject', 'Manny', 'MannyLocation',
           'ProbeInfo', 'Player', 'CraftingRecipe', 'CraftingOutput', 'CraftingIngredient', 'ProbeType', 'BaseProbe', 'SectorProbePresence',
           'Movement', 'Probe', 'SectorObservationProbeDistance', 'OutOfRangeProbe', 'Fuel', 'ScutNetworkReference', 'ProbeModel',
           'StorageContainerRules', 'ContainerKind', 'ContainerMeta', 'StorageContainer', 'ItemKind', 'Item', 'ResourceStockContainer',
           'CapacityUnit', 'ProbeInventory', 'ProbeSystems', 'ProbeNavigation', 'ProbeTerminalAlert', 'ProbeTerminalAlertAction',
           'ProbeSensorMode', 'ProbeExternalTank', 'MannyCargo', 'ResourceStock', 'ProbeStatus', 'ProbeSummary', 'ProbeSummaryList', 'RadiusUnit',
           'ResourceType', 'Player', 'APIKey', 'Printable', 'PrintResponse', 'MissileState', 'ProbeSectorResponse',
           'AutonomousUnitObservationResponse', 'AutonomousUnitCarrier', 'AutonomousUnitObservation', 'Mission', 'MissionStep',
           'MessageEndpoint', 'Message', 'MessageResponse', 'Pagination', 'ScutNetworkProbe', 'ProbeImprovement', 'ProbeImprovementId',
           'ProbeImprovementIngredient', 'ObservedClass', 'BlueprintReference', 'ProbeReference', 'ProbeImprovementBlueprintShareResponse',
           'InventoryBrief', 'StorageContainerInventoryResponse', 'CraftingReservationResponse', 'CraftingReassignment', 'ProbeAlertResponse',
           'Alert', 'AlertDataBlueprint', 'AlertDataInstanceSwitch', 'AlertDataContainer', 'AlertDataObject', 'AlertDataReport', 'AlertDataPlanet',
           'AlertDataRisk', 'AlertDataProbeDestroyed', 'AlertRules', 'AlertType', 'ProbeDestroyedReason', 'ProbeDamageWarningRule', 'MessageStatus',
           'ProbeDamageWarningResponse', 'Session', 'ProbeInventoryJettisonResponse', 'Jettisoned', 'StorageMoveResponse', 'AsteroidSpeed',
           'ProbeMindSnapshotReassignResponse', 'LogbookPage', 'LogbookPageSummary', 'ProbeLogbookPagesResponse', 'AsteroidTrajectory']

from dataclasses import dataclass, field
from mashumaro import DataClassDictMixin
from typing import List, Dict, Any, Literal, Union
from datetime import datetime


type ProbeModel = Union[Literal['generic', 'deuterium_tanker'], str]
type ProbeSensorMode = Union[Literal['normal', 'degraded', 'blind'], str]
type CapacityUnit = Union[Literal['earth_container_equivalent'], str]
type ContainerKind = Union[Literal['probe', 'container'], str]
type ItemKind = Union[Literal['waypoint_bookmark', 'steel_bar', 'steel_plate', 'additional_container', 'micro_conductor', 'ceramic_insulator',
                              'crystal_substrate', 'dopant_matrix', 'integrated_circuit', 'electric_motor', 'battery_pack', 'linear_actuator',
                              'atomic_printer_part', 'deuterium_engine', 'solar_panel', 'scut_relay', 'scut_transit_beacon',
                              'thermal_protection_shell', 'parachute_pack', 'descent_guidance_module', 'atmospheric_drop_kit', 'missile', 'manny'],
                      str]
type ProbeStatus = Union[Literal['idle', 'preparing', 'accelerating', 'cruising', 'decelerating', 'orbiting',
                                 'disabled', 'dead', 'trapped_by_black_hole'], str]
type RadiusUnit = Union[Literal['solar_radius', 'earth_radius', 'kilometer', 'astronomical_unit', 'meter'], str]
type ResourceType = Union[Literal['deuterium', 'metals', 'ice', 'carbon_compounds'], str]
type ObservedClass = Union[Literal['suspected_missile', 'large_ship', 'ship'], str]
type Printable = Union[Literal['micro_conductor', 'ceramic_insulator', 'crystal_substrate',
                               'dopant_matrix', 'integrated_circuit', 'atomic_printer_part'], str]
type ProbeImprovementId = Union[Literal['deuterium_compression', 'reinforced_container_couplings',
                                        'distributed_thrust_anchoring', 'anatiform_asteroid_sculpting'], str]
type AlertType = Union[Literal['storage_container_break', 'intelligent_life', 'sector_object_detected', 'manny_report', 'anomaly_detected',
                               'mind_snapshot_transferred', 'probe_destroyed', 'asteroid_trajectory', 'blueprint_shared', 'others_presence',
                               'others_weapon', 'others_harvest_traces'], str]
type MessageStatus = Union[Literal['unread', 'read'], str]
type ProbeDestroyedReason = Union[Literal['black_hole_trap', 'movement_collision'], str]


@dataclass
class Player(DataClassDictMixin):
    id: int
    username: str
    forumAdmin: bool
    forumModerator: bool
    displayName: str | None = None


@dataclass
class Vector(DataClassDictMixin):
    x: int
    y: int
    z: int

    def __iter__(self):
        return iter([self.x, self.y, self.z])


@dataclass
class Sector(DataClassDictMixin):
    relative: Vector


@dataclass
class SectorVisitHistory(DataClassDictMixin):
    relativeCoordinates: Vector
    firstVisitedAt: datetime
    lastVisitedAt: datetime
    visitCount: int


@dataclass
class ResourceAmounts(DataClassDictMixin):
    deuterium: float
    metals: float
    ice: float
    carbon_compounds: float


@dataclass
class WaypointBookmark(DataClassDictMixin):
    name: str
    playerId: int
    playerName: str
    createdAt: datetime


@dataclass
class AsteroidSpeed(DataClassDictMixin):
    sectors: int
    perSeconds: int


@dataclass
class AsteroidTrajectory(DataClassDictMixin):
    id: str
    asteroidId: str
    mode: Literal['system_impact', 'sector_transfer'] | str
    status: Literal['accelerating', 'coasting', 'crossing_sector', 'orbiting_black_hole', 'captured', 'completed', 'missed', 'no_effect',
                    'destroyed', 'lost', 'failed'] | str
    startedAt: datetime
    nextTransitionAt: datetime
    targetobjectId: str | None = None
    targetSpeedC: float | None = None
    currentSpeedC: float | None = None
    plannedRevolutions: int | None = None
    completedRevolutions: int | None = None
    estimatedCompletionAt: datetime | None = None
    speed: AsteroidSpeed | None = None
    direction: Vector | None = None
    sectorsCrossed: int | None = None
    maximumSectorCrossings: int | None = None
    result: str | None = None
    failureReason: str | None = None


@dataclass
class MineableSectorObject(DataClassDictMixin):
    id: str
    type: str
    name: str | None
    mass: float
    resources: List[str]
    resourceTypes: List[str]
    resourceComposition: ResourceAmounts
    massUnit: str | None = None
    radius: float | None = None
    radiusUnit: str | None = None
    resourceAmounts: ResourceAmounts | None = None
    composition: str | None = None
    sizeCategory: str | None = None
    motorized: bool | None = None
    motorFuelStatus: str | None = None
    capturedByObjectId: str | None = None
    distinctiveFeature: str | None = None
    trajectory: AsteroidTrajectory | None = None
    category: str | None = None
    habitabilityScore: float | None = None
    waypointBookmarks: List[WaypointBookmark] | None = None


@dataclass
class BookmarkableSectorObject(DataClassDictMixin):
    id: str
    type: str
    name: str | None
    mass: float | None = None
    massUnit: str | None = None
    radius: float | None = None
    radiusUnit: str | None = None
    category: str | None = None
    habitabilityScore: float | None = None
    motorized: bool | None = None
    motorFuelStatus: str | None = None
    capturedByObjectId: str | None = None
    distinctiveFeature: str | None = None
    trajectory: AsteroidTrajectory | None = None
    waypointBookmarks: List[WaypointBookmark] | None = None


@dataclass
class ScutNetworkReference(DataClassDictMixin):
    id: str
    name: str


@dataclass
class MannyCargo(DataClassDictMixin):
    capacity: float
    deuterium: float
    metals: float
    ice: float
    organicCompounds: float
    capacityUnit: CapacityUnit


@dataclass
class Movement(DataClassDictMixin):
    direction: Vector


@dataclass
class SectorObject(DataClassDictMixin):
    id: str
    """Opaque object id. Clients must not parse coordinates from it. 
    For scut_relay objects this is the relay integer id serialized as a string; 
    pass it as an integer relayId to turn-on-relay or install-scut-transit-beacon."""
    summary: str
    name: str | None = None
    """Public object label. Generated asteroids have a short content-based name such as Ice Deut 15ce. 
    For inhabited planets, generated or debug names that would reveal absolute coordinates are replaced by a player-relative label."""
    type: Literal['star', 'planet', 'asteroid', 'dust_cloud', 'black_hole', 'solar_system', 'manny', 'drifting_item', 'detached_container',
                  'deuterium_refuel_station', 'dormant_construct', 'scut_relay', 'missile'] | str | None = None
    estimated: bool | None = None
    mass: float | None = None
    massUnit: Literal['solar_mass', 'earth_mass', 'kilogram'] | str | None = None
    """Unit used by mass when present. Stars, black holes and dust clouds use solar_mass; planets and asteroids use earth_mass."""
    radius: float | None = None
    radiusUnit: RadiusUnit | None = None
    """Unit used by radius when present. Stars use solar_radius; planets and asteroids use earth_radius; 
    black holes use kilometer; solar systems and dust clouds use astronomical_unit."""
    dangerLevel: Literal['low', 'moderate', 'extreme'] | str | None = None
    starCount: int | None = None
    """Present on solar systems."""
    planetCount: int | None = None
    """Present on solar systems."""
    orbitalBodyCount: int | None = None
    """Present on solar systems."""
    resources: List[str] | None = None
    resourceTypes: List[ResourceType] | None = None
    """Present on planets, asteroids, and deuterium refuel stations; use mineable object values in MannyMineRequest.resources."""
    resourceComposition: ResourceAmounts | None = None
    """Normalized mineable-resource shares. Values are rounded to four decimals and normally sum to 1 when at least one resource is present."""
    resourceAmounts: ResourceAmounts | None = None
    """Remaining material reserves in equivalent earth containers. Asteroids expose this exact four-key object; mining subtracts from these values."""
    mannyMineable: bool | None = None
    """Present on planets and asteroids; true when a Manny can mine this object."""
    composition: str | None = None
    """Present on asteroids; generator composition class such as iron, silicate, carbonaceous, ice or rare_metals."""
    motorized: bool | None = None
    """Present on asteroid objects; true once Distributed Thrust Anchoring propulsion is installed."""
    motorFuelStatus: Literal['full', 'empty'] | str | None = None
    """Present only on motorized asteroids."""
    capturedByObjectId: str | None = None
    """Present when the asteroid is captured by another local celestial object."""
    distinctiveFeature: Literal['Sculpted in the shape of a duck'] | None = None
    """Present only on duck-shaped asteroids; omitted from ordinary asteroid objects."""
    inTransit: bool | None = None
    """Present and true for a sector-transfer asteroid between two phase transitions."""
    trajectory: AsteroidTrajectory | None = None
    launcherKind: Literal['probe', 'others_ship'] | None = None
    """Present only for moving missile objects."""
    targetKind: Literal['probe', 'others_ship', 'others_auxiliary', 'manny', 'missile', 'motorized_asteroid'] | str | None = None
    """Present only for moving missile objects."""
    targetId: str | None = None
    """Opaque public target id, present only for moving missile objects."""
    launchedAt: datetime | None = None
    """Present only for moving missile objects."""
    impactAt: datetime | None = None
    """Estimated resolution time, present only for moving missile objects."""
    targetsCurrentProbe: bool | None = None
    """Present on moving missiles in probe-scoped current-sector scans; true only when the observing probe is the missile target."""
    category: str | None = None
    """Present on planets."""
    habitabilityScore: float | None = None
    """Present on planets in detailed current-sector or already-visited-sector observations."""
    salvageable: bool | None = None
    """True when the object can be recovered with POST /api/probe/mannies/{mannyId}/salvage. 
    Drifting item stacks expose true only when each unit fits within Manny cargo capacity. 
    Detached containers expose true only when mode is drifting; hidden_on_asteroid containers must be recovered with 
    POST /api/probe/mannies/{mannyId}/recover-storage-container."""
    waypointBookmarks: List[WaypointBookmark] | None = None
    bookmarkTargets: List[BookmarkableSectorObject] | None = None
    """Present on solar systems; lists nested stars and orbital bodies that can receive a waypoint bookmark."""
    minableTargets: List[MineableSectorObject] | None = None
    """Present on solar systems; lists nested planets/asteroids that can be mined by a Manny."""
    mannyState: Literal['abandoned', 'forgotten'] | None = None
    """Present only for detected Manny objects in the current sector."""
    mannyUid: str | None = None
    """Present only for detected Manny objects."""
    cargo: MannyCargo | None = None
    """Present only for detected Manny objects."""
    itemType: str | None = None
    """Present only for drifting item stacks."""
    quantity: int | None = None
    """Present only for drifting item stacks."""
    containerSpace: float | None = None
    """Per-item storage space for drifting item stacks."""
    mode: Literal['[drifting', 'hidden_on_asteroid'] | str | None = None
    """Present only for detached containers. Hidden containers are included only for players who have discovered them."""
    targetObjectId: str | None = None
    """Present for detached containers, null unless the container is attached to another sector object."""
    capacity: float | None = None
    """Storage capacity for detached container objects."""
    capacityUnit: CapacityUnit | None = None
    planetId: str | None = None
    """Present only for deuterium refuel stations; id of the planet that placed the station in orbit."""
    planetName: str | None = None
    """Present only for deuterium refuel stations; public name of the planet that placed the station."""
    apparentOrigin: Literal['unknown_non_natural'] | str | None = None
    """Present only for dormant_construct objects."""
    activityStatus: Literal['dormant'] | str | None = None
    """Present only for dormant_construct objects."""
    knownFunction: Literal['unknown'] | str | None = None
    """Present only for dormant_construct objects; 
    detailed scans cannot determine whether the structure is a vessel, factory, or another kind of utility."""
    status: Literal['off', 'on', 'moving'] | str | None = None
    """Relay activation state for SCUT relays, or `moving` for an in-flight missile."""
    createdByProbeId: int | None = None
    """Present only for SCUT relay objects."""
    createdByProbeName: str | None = None
    """Present only for SCUT relay objects; probe name when the creator still exists, 
    "death probe" when createdByProbeId points to a deleted probe, null when no creator was recorded."""
    activatedAt: datetime | None = None
    """Present only for SCUT relay objects."""
    coverageRadiusSectors: int | None = None
    """Present only for SCUT relay objects."""
    network: ScutNetworkReference | None = None
    """Present only for SCUT relay objects."""
    kind: str | None = None
    observedClass: ObservedClass | None = None
    """Present on detected missiles and Others ships."""
    movement: Movement | None = None
    summary: str | None = None


@dataclass
class SectorScan(DataClassDictMixin):
    currentSectorResidenceSeconds: int
    requiredResidenceSeconds: int
    scanQuality: int


@dataclass
class ScutRelay(DataClassDictMixin):
    id: int
    type: str
    name: str
    coverageRadiusSectors: int
    sector: Sector


@dataclass
class ScutNetworkProbe(DataClassDictMixin):
    id: int
    name: str
    sector: Sector


@dataclass
class ScutNetwork(DataClassDictMixin):
    id: int
    name: str
    createdAt: datetime
    updatedAt: datetime
    relayCount: int
    coveredSectorCount: int
    relays: List[ScutRelay]
    probes: List[ScutNetworkProbe]


@dataclass
class SectorProbePresence(DataClassDictMixin):
    id: str
    name: str
    moving: bool
    owned: bool
    """True when the detected probe belongs to the authenticated player."""


@dataclass
class SectorObservationProbeDistance(DataClassDictMixin):
    probeId: int
    probeName: str
    distance: int
    isDefault: bool
    usedForScan: bool


@dataclass
class SectorObservation(DataClassDictMixin):
    relativeCoordinates: Vector
    distance: int
    knowledgeLevel: Literal['detailed', 'neighbor_scan', 'distant_scan', 'long_range_estimation'] | str
    confidence: float
    scan: SectorScan
    sensorMode: Literal['normal', 'degraded', 'blind'] | str
    dataFreshness: Literal['live', 'degraded_live', 'historical', 'unavailable'] | str
    distances: List[SectorObservationProbeDistance] | None = None
    objects: List[SectorObject] | None = None
    probes: List[SectorProbePresence] | None = None
    scutNetworks: List[ScutNetworkReference] | None = None
    scutCoverageStatus: Literal['covered', 'uncovered', 'unknown'] | str | None = None
    estimatedObjects: Dict[Any, Any] | None = None
    possibleObjects: List[str] | None = None
    navigationalRisk: str | None = None
    message: str | None = None


@dataclass
class MannyLocation(DataClassDictMixin):
    type: Literal['probe', 'sector'] | str
    sector: Sector | None = None


@dataclass
class Manny(DataClassDictMixin):
    id: str
    name: str
    location: MannyLocation
    currentTask: str | None
    taskProgressPercent: float
    taskEstimatedEndTime: str
    taskStartTime: str
    task: Dict | None | List


@dataclass
class ProbeInfo(DataClassDictMixin):
    id: int
    name: str
    status: str
    isDefault: bool
    isReachable: bool


@dataclass
class CraftingIngredient(DataClassDictMixin):
    type: str
    quantity: int | float
    unit: str
    kind: str


@dataclass
class CraftingOutput(DataClassDictMixin):
    type: str
    name: str
    containerSpace: float
    containerSpaceUnit: str
    cargoCapacity: float | None = None
    cargoCapacityUnit: str | None = None
    capacityBonus: float | None = None
    capacityBonusUnit: str | None = None


@dataclass
class CraftingRecipe(DataClassDictMixin):
    id: ItemKind
    name: str
    description: str
    craftableBy: List[str]
    ingredients: List[CraftingIngredient]
    durationSeconds: int
    output: CraftingOutput


@dataclass
class Fuel(DataClassDictMixin):
    deuterium: float
    maxDeuterium: float


@dataclass
class Movement(DataClassDictMixin):
    status: Literal['preparing', 'accelerating', 'cruising', 'decelerating', 'arrived', 'failed', 'destroyed'] | str
    origin: Vector
    target: Vector
    distance: int
    fuelCostDeuterium: float
    """Fixed deuterium-point cost reserved at departure for the complete trip, including deceleration."""
    startedAt: datetime
    arrivalAt: datetime
    phase: Literal['idle', 'preparing', 'accelerating', 'cruising', 'decelerating', 'arrived', 'failed', 'destroyed'] | str | None = None
    secondsRemaining: int | None = None
    sensorMode: ProbeSensorMode | None = None
    estimatedVelocityC: float | None = None


@dataclass
class BaseProbe(DataClassDictMixin):
    id: int
    name: str
    status: ProbeStatus


@dataclass
class OutOfRangeProbe(BaseProbe, DataClassDictMixin):
    sector: Sector


@dataclass
class ProbeNavigation(DataClassDictMixin):
    velocityC: float
    accelerationCPerDay: float
    direction: Vector


@dataclass
class ProbeSystems(DataClassDictMixin):
    integrityPercent: float
    energyStored: float
    internalClockRate: float
    currentTask: str | None


@dataclass
class ProbeTerminalAlertAction(DataClassDictMixin):
    label: str
    method: str
    endpoint: str


@dataclass
class ProbeTerminalAlert(DataClassDictMixin):
    type: Literal['mind_snapshot_reassignment_available'] | str
    severity: Literal['critical'] | str
    title: str
    message: str
    """Public alert text. Sector coordinates in messages are expressed relative to the player reference frame and must not expose 
    absolute sector coordinates. An asteroid_trajectory ignition alert for system_impact identifies the opaque target id and its type."""
    action: ProbeTerminalAlertAction


@dataclass
class ProbeExternalTank(DataClassDictMixin):
    id: str
    type: Literal['deuterium'] | str
    name: str
    fillPercent: float
    external: bool
    usesCargoCapacity: bool


@dataclass
class ContainerMeta(DataClassDictMixin):
    id: str
    kind: ContainerKind
    label: str
    sortOder: int | None = None


@dataclass
class Item(DataClassDictMixin):
    id: str
    type: ItemKind
    name: str
    containerSpace: float
    """Space occupied in equivalent earth containers."""
    currentTask: str | None = None
    taskProgressPercent: float | None = None
    location: MannyLocation | None = None
    cargo: MannyCargo | None = None
    container: ContainerMeta | None = None
    metadata: dict | None = None


@dataclass
class ResourceStockContainer(DataClassDictMixin):
    container: ContainerMeta
    amount: float
    containerSpace: float
    capacityUnit: CapacityUnit


@dataclass
class ResourceStock(DataClassDictMixin):
    id: str
    type: Literal['metals', 'ice', 'carbon_compounds'] | str
    name: str
    amount: float
    containerSpace: float
    capacityUnit: CapacityUnit
    containers: List[ResourceStockContainer]


@dataclass
class StorageContainerRules(DataClassDictMixin):
    priority: List[str] = field(default_factory=list)
    exclusion: List[str] = field(default_factory=list)
    strictExclusion: List[str] = field(default_factory=list)


@dataclass
class StorageContainer(DataClassDictMixin):
    id: str
    kind: ContainerKind
    label: str
    capacity: float
    usedCapacity: float
    freeCapacity: float
    capacityUnit: CapacityUnit
    rules: StorageContainerRules
    sortOder: int | None = None


@dataclass
class ProbeInventory(DataClassDictMixin):
    capacity: float
    """Maximum transport capacity in equivalent earth containers."""
    capacityUnit: CapacityUnit
    usedCapacity: float
    freeCapacity: float
    items: List[Item]
    resourceStocks: List[ResourceStock]
    containers: List[StorageContainer]
    """Probe core and additional storage containers, including their routing rules."""
    externalTanks: List[ProbeExternalTank]
    """Special external tanks that do not consume cargo capacity."""


@dataclass
class Probe(BaseProbe, DataClassDictMixin):
    model: ProbeModel
    fuel: Fuel
    sensorMode: ProbeSensorMode
    sector: Sector | None
    alert: ProbeTerminalAlert | None = None
    movement: Movement | None = None
    navigation: ProbeNavigation | None = None
    systems: ProbeSystems | None = None
    inventory: ProbeInventory | None = None
    message: str | None = None


ProbeType = Union[OutOfRangeProbe, Probe]


@dataclass
class ProbeSummary(DataClassDictMixin):
    id: int
    name: str
    model: ProbeModel
    status: ProbeStatus
    isDefault: bool
    isReachable: bool
    """True when the probe is the default probe, in the same sector as the default probe, or inside shared active SCUT network coverage."""


@dataclass
class ProbeSummaryList(DataClassDictMixin):
    defaultProbeId: int | None
    """Identifier of the player's default probe."""
    probes: List[ProbeSummary]


@dataclass
class Player(DataClassDictMixin):
    id: int
    username: str
    forumAdmin: bool
    forumModerator: bool
    displayName: str | None = None


@dataclass
class APIKey(DataClassDictMixin):
    id: int
    token: str
    """Clear API key shown only once. Use it as the Bearer token."""
    label: str
    lastFour: str
    createdAt: datetime


@dataclass
class PrintResponse(DataClassDictMixin):
    manny: Manny
    inventory: ProbeInventory


@dataclass
class MissileState(DataClassDictMixin):
    id: str
    launcherKind: str
    launcherId: str
    targetId: str
    status: str
    launchedAt: datetime
    createdAt: datetime
    updatedAt: datetime
    impactAt: datetime | None = None
    result: str | None = None
    actionId: str | None = None
    details: Dict[Any, Any] | None = None


@dataclass
class ProbeSectorResponse(DataClassDictMixin):
    sector: SectorObservation
    inventory: ProbeInventory

    def __iter__(self):
        return iter([self.sector, self.inventory])


@dataclass
class AutonomousUnitCarrier(DataClassDictMixin):
    id: str
    kind: Literal['probe', 'others_ship'] | str


@dataclass
class AutonomousUnitObservation(DataClassDictMixin):
    id: str
    """Opaque public identifier of the deployed unit."""
    kind: Literal['manny', 'others_auxiliary'] | str
    carrier: AutonomousUnitCarrier
    spatialState: Literal['moving_to_sector_object', 'returning_to_carrier', 'drifting', 'landed_on_sector_object']


@dataclass
class AutonomousUnitObservationResponse(DataClassDictMixin):
    autonomousUnits: List[AutonomousUnitObservation]
    nextCursor: str | None = None
    """Opaque cursor for the next page. Omitted on the last page."""


@dataclass
class MissionStep(DataClassDictMixin):
    id: str
    sortOrder: int
    tite: str
    description: str
    status: Literal['pending', 'completed', 'failed', 'skipped']
    metadata: Dict[Any, Any]
    createdAt: datetime
    updatedAt: datetime | None = None
    completedAt: datetime | None = None
    failedAt: datetime | None = None


@dataclass
class Mission(DataClassDictMixin):
    id: str
    """Stable public mission id"""
    type: str
    """Mission family identifier, chosen by the event that creates the mission. 
    First-contact intelligent-life scenarios currently use `first_contact.return_to_space_program`."""
    title: str
    description: str
    status: Literal['active', 'completed', 'failed', 'abandoned']
    stepOrder: Literal['free', 'sequential']
    metadata: Dict[Any, Any]
    """Public mission metadata. Sector coordinates, when present, are exposed as player-relative coordinates under `sector.relative`; 
    inhabited-planet names that would reveal absolute coordinates are replaced by a public label."""
    startedAt: datetime
    createdAt: datetime
    updatedAt: datetime | None
    steps: List[MissionStep]
    createdByEvent: Dict[Any, Any] | None = None
    """Public mission creation context. Sector coordinates, when present, are exposed as player-relative coordinates under `sector.relative`."""
    completedAt: datetime | None = None
    failedAt: datetime | None = None
    abandonedAt: datetime | None = None


@dataclass
class MessageEndpoint(DataClassDictMixin):
    type: Literal['probe', 'planet', 'unknown']
    id: str | int
    """Numeric probe id for probe endpoints, opaque planet object id for planet endpoints, or opaque sender id for unknown endpoints. 
    Planet ids must not be interpreted as coordinates."""
    name: str
    """Public endpoint label. Planet endpoint names that would reveal absolute coordinates are replaced by a public label; 
    unknown endpoints may use a generic sender label."""
    probeId: int | None = None
    """Present when `type` is `probe`."""
    planetId: str | None = None
    """Present when `type` is `planet`."""


@dataclass
class Message(DataClassDictMixin):
    id: int
    sender: MessageEndpoint
    recipient: MessageEndpoint
    sector: Sector
    body: str
    status: MessageStatus
    readAt: datetime | None
    createdAt: datetime
    updatedAt: datetime | None


@dataclass
class Pagination(DataClassDictMixin):
    limit: int
    offset: int
    count: int
    total: int
    hasMore: bool


@dataclass
class MessageResponse(DataClassDictMixin):
    messages: List[Message]
    pagination: Pagination


@dataclass
class ProbeImprovementIngredient(DataClassDictMixin):
    type: str
    quantity: int | float
    unit: str
    kind: Literal['item', 'resource']


@dataclass
class ProbeImprovement(DataClassDictMixin):
    id: ProbeImprovementId
    name: str
    description: str
    available: bool
    """Whether the selected probe owner's player knows this improvement blueprint."""
    done: bool
    """Whether the improvement effect has already been installed on the selected probe."""
    installableOnProbe: bool
    """Whether this blueprint describes an improvement installed on probes. 
    False for action blueprints such as distributed_thrust_anchoring and anatiform_asteroid_sculpting."""
    durationSeconds: int
    ingredients: List[ProbeImprovementIngredient]
    effects: Dict[Any, Any]
    createdAt: datetime | None = None
    updatedAt: datetime | None = None


@dataclass
class BlueprintReference(DataClassDictMixin):
    id: ProbeImprovementId
    name: str


@dataclass
class ProbeReference(DataClassDictMixin):
    id: int
    name: str


@dataclass
class ProbeImprovementBlueprintShareResponse(DataClassDictMixin):
    blueprint: BlueprintReference
    recipientProbe: ProbeReference
    alreadyKnown: bool
    """True when the recipient player already owned the blueprint before this request."""
    recipientNotified: bool
    """Confirms that a persistent recipient alert exists; retries do not duplicate it."""


@dataclass
class InventoryBrief(DataClassDictMixin):
    capacityUnit: CapacityUnit
    items: List[Item]
    resourceStorcks: List[ResourceStock]


@dataclass
class StorageContainerInventoryResponse(DataClassDictMixin):
    container: StorageContainer
    inventory: InventoryBrief


@dataclass
class CraftingReassignment(DataClassDictMixin):
    mannyId: str
    containerId: str


@dataclass
class CraftingReservationResponse(DataClassDictMixin):
    reassignmentCount: int
    reassignments: List[CraftingReassignment]


@dataclass
class ProbeDamageWarningRule(DataClassDictMixin):
    type: Literal['storage_container_break'] | str
    startsAtAdditionalContainers: int
    maximumRiskPercent: int
    message: str


@dataclass
class AlertRules(DataClassDictMixin):
    storageContainerBreak: ProbeDamageWarningRule


@dataclass
class AlertDataBlueprint(DataClassDictMixin):
    blueprintId: ProbeImprovementId
    recipientProbe: ProbeReference


@dataclass
class AlertDataProbeDestroyed(DataClassDictMixin):
    probeId: int
    reason: ProbeDestroyedReason


@dataclass
class AlertDataInstanceSwitch(DataClassDictMixin):
    previousProbeId: int
    reason: ProbeDestroyedReason


@dataclass
class AlertDataReport(DataClassDictMixin):
    title: str
    objectId: str | None
    objectType: str
    objectLabel: str


@dataclass
class AlertDataObject(DataClassDictMixin):
    id: str
    type: str
    label: str
    resourceTypes: List[ResourceType]


@dataclass
class AlertDataPlanet(DataClassDictMixin):
    id: str
    name: str | None


@dataclass
class AlertDataRisk(DataClassDictMixin):
    percent: int
    addicionalContainerCount: int
    ruleStartsAtAdditionalContainers: int | None = None


@dataclass
class AlertDataContainer(DataClassDictMixin):
    id: str
    label: str
    objectId: str


@dataclass
class Alert(DataClassDictMixin):
    id: int
    type: AlertType
    status: MessageStatus
    message: str
    illustrationImageUrl: str | None
    phase: Literal['acceleration_end', 'deceleration_start', 'arrival', 'detection', 'manny_report', 'instance_switch', 'probe_loss', 'ignition',
                   'blueprint_share', 'weapon', 'weapon_targeted', 'weapon_result', 'weapon_damage'] | str
    scheduledAt: datetime
    createdAt: datetime
    updatedAt: datetime | None
    readAt: datetime | None
    resolvedAt: datetime | None
    sector: Sector
    container: AlertDataContainer | None = None
    """Present for `storage_container_break` alerts."""
    risk: AlertDataRisk | None = None
    """Present for `storage_container_break` alerts."""
    planet: AlertDataPlanet | None = None
    """Present for `intelligent_life` alerts."""
    object: AlertDataObject | None = None
    """Present for `sector_object_detected` alerts."""
    report: AlertDataReport | None = None
    """Present for `manny_report` alerts."""
    instanceSwitch: AlertDataInstanceSwitch | None = None
    """Present for `mind_snapshot_transferred` alerts."""
    destroyedProbe: AlertDataProbeDestroyed | None = None
    """Present for `probe_destroyed` alerts."""
    blueprintShare: AlertDataBlueprint | None = None
    """Present for `blueprint_shared` alerts."""


@dataclass
class ProbeAlertResponse(DataClassDictMixin):
    alerts: List[Alert]
    rules: AlertRules


@dataclass
class ProbeDamageWarningResponse(DataClassDictMixin):
    damageWarnings: List[Alert]
    rules: ProbeDamageWarningRule


@dataclass
class Session(DataClassDictMixin):
    token: str
    expiresAt: datetime
    player: Player


@dataclass
class Jettisoned(DataClassDictMixin):
    type: ItemKind | ResourceType | None = None
    amount: float | int | None = None
    """Present for discarded resources and deuterium."""
    quantity: int | None = None
    """Present for crafted items added to a drifting sector stack."""
    driftingQuantity: int | None = None
    """Total quantity of this crafted item type now drifting in the current sector."""
    objectId: str | None = None
    """Current-sector drifting item object id for crafted item jettison, or SCUT relay object id for scut_relay jettison."""
    status: Union[Literal['off'], str] | None = None
    """Present for scut_relay jettison."""
    containerSpace: float | None = None


@dataclass
class ProbeInventoryJettisonResponse(DataClassDictMixin):
    inventory: ProbeInventory
    jettisoned: Jettisoned | None = None
    many: Manny | None = None


@dataclass
class StorageMoveResponse(DataClassDictMixin):
    manny: Manny
    inventory: ProbeInventory


@dataclass
class ProbeMindSnapshotReassignResponse(DataClassDictMixin):
    reassigned: bool
    previousProbeId: int
    probe: Probe
    message: str


@dataclass
class LogbookPageSummary(DataClassDictMixin):
    id: int
    probeId: int
    title: str
    sortOrder: int
    createdAt: datetime
    updatedAt: datetime


@dataclass
class LogbookPage(LogbookPageSummary):
    content: str


@dataclass
class ProbeLogbookPagesResponse(DataClassDictMixin):
    pages: List[LogbookPageSummary]
    pagination: Pagination
