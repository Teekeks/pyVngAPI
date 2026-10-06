from typing import List

from vng_api.base import APISub, APIResponse
from vng_api.helper.internal import build_url
from vng_api.types import ProbeSectorResponse, SectorVisitHistory, AutonomousUnitObservationResponse, SectorStorageInventory


class ProbeSectorSub(APISub):

    async def get(self, pid: int) -> APIResponse[ProbeSectorResponse]:
        """Get observable probe sector and onboard inventory

        :param pid: Probe ID
        """
        data = await self.client.api_call('get', f'probe/{pid}/sector', None,
                                          lambda inp: ProbeSectorResponse.from_dict(inp))
        if data.success:
            await self.client.issue_cache_update(data.data.sector)
            await self.client.issue_cache_update(data.data.inventory)
        return data

    async def get_visited(self, pid: int) -> APIResponse[List[SectorVisitHistory]]:
        """List sectors already visited by the requested probe

         Returns only the requested probe's visited-sector history.
         Coordinates are relative to the player's home sector and sorted by most recent visit first.

        :param pid: Probe ID
        """
        return await self.client.api_call('get',
                                          f'probe/{pid}/visited-sectors',
                                          None,
                                          lambda inp: [SectorVisitHistory.from_dict(v) for v in inp['visitedSectors']])

    async def autonomous_units(self, pid: int, limit: int | None = None, cursor: str | None = None) -> APIResponse[AutonomousUnitObservationResponse]:
        """Observe autonomous units deployed in the probe sector

        Returns every deployed Manny and active Others auxiliary physically present in the selected probe's current sector, regardless of the
        unit's owner. The observer probe must belong to the authenticated player and must not be dead or moving.
        Absolute sector coordinates are never exposed.

        :param pid: Probe ID
        :param limit: Maximum number of autonomous units to return. Min: 1, Max: 500, Default: 100
        :param cursor: Opaque cursor returned as `nextCursor` by the preceding page.
        """
        url = build_url(f'probe/{pid}/sector/autonomous-units', {'limit': limit, 'cursor': cursor})
        return await self.client.api_call('get', url, None,
                                          lambda inp: AutonomousUnitObservationResponse.from_dict(inp))

    async def get_object_inventory(self,
                                   pid: int,
                                   object_id: str,
                                   limit: int = None,
                                   cursor: str = None) -> APIResponse[SectorStorageInventory]:
        """Read accessible sector storage contents

        Available for drifting containers, personally known containers hidden on asteroids, and other storage
        objects whose access this probe has discovered. Items are individually selectable; the container shell is
        excluded. Access is revalidated on every page. No absolute coordinates are returned.

        :param pid: Probe ID
        :param object_id: ID of object with storage in sector
        :param limit: Maximum number of items to return. Default: 100, Max: 500, Min: 1
        :param cursor: Cursor for pagination
        """
        url = build_url(f'probe/{pid}/sector-objects/{object_id}/inventory', {'limit': limit, 'cursor': cursor})
        return await self.client.api_call('get', url, None, lambda inp: SectorStorageInventory.from_dict(inp))
