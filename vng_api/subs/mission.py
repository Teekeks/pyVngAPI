from typing import List

from vng_api.base import APISub, APIResponse
from vng_api.types import Mission


class MissionSub(APISub):

    async def get_all(self) -> APIResponse[List[Mission]]:
        """List active player missions

        Returns missions currently assigned to the authenticated player.
        """
        return await self.client.api_call('get', 'probe/missions', None,
                                          lambda inp: [Mission.from_dict(x) for x in inp['missions']])
