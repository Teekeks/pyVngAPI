from typing import List

from vng_api.base import APISub, APIResponse
from vng_api.types import ProbeSectorResponse, SectorVisitHistory


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
