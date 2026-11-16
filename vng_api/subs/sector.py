__all__ = ['SectorSub']

from typing import List

from vng_api.base import APISub, APIResponse
from vng_api.types import SectorVisitHistory, SectorObservation


class SectorSub(APISub):

    async def get(self, x: int, y: int, z: int) -> APIResponse[SectorObservation]:
        """Get a sector observation.

        :param x: X coordinate of the target sector
        :param y: Y coordinate of the target sector
        :param z: Z coordinate of the target sector
        """
        return await self.client.api_call('get',
                                          f'sector?x={x}&y={y}&z={z}',
                                          None,
                                          lambda inp: SectorObservation.from_dict(inp['sector']))

    async def get_visited(self) -> APIResponse[List[SectorVisitHistory]]:
        """Get all sector visit history."""
        return await self.client.api_call('get',
                                          'visited-sectors',
                                          None,
                                          lambda inp: [SectorVisitHistory.from_dict(v) for v in inp['visitedSectors']])
