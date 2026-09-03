from typing import List

from vng_api.base import APISub, APIResponse
from vng_api.types import SectorVisitHistory, SectorObservation

__all__ = ['SectorSub']


class SectorSub(APISub):

    async def get(self, x: int, y: int, z: int) -> APIResponse[SectorObservation]:
        return await self.client.api_call('get',
                                          f'sector?x={x}&y={y}&z={z}',
                                          None,
                                          lambda inp: SectorObservation.from_dict(inp['sector']))

    async def get_visited(self) -> APIResponse[List[SectorVisitHistory]]:
        return await self.client.api_call('get',
                                          'visited-sectors',
                                          None,
                                          lambda inp: [SectorVisitHistory.from_dict(v) for v in inp['visitedSectors']])
