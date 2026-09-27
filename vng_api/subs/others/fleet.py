from typing import List

from vng_api.base import APISub, APIResponse
from vng_api.types.others import OthersFleet, OthersFleetSummary


class OthersFleetSub(APISub):

    async def get(self, fid: str) -> APIResponse[OthersFleet]:
        """Get one owned fleet

        :param fid: Fleet ID
        """
        return await self.client.api_call('get', f'others/fleets/{fid}', None, lambda inp: OthersFleet.from_dict(inp['fleet']))

    async def get_summary_list(self) -> APIResponse[List[OthersFleetSummary]]:
        """List owned Others fleets"""
        return await self.client.api_call('get', 'others/fleets', None,
                                          lambda inp: [OthersFleetSummary.from_dict(x) for x in inp['fleets']])

