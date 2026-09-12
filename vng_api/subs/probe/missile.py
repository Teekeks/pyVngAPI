from vng_api.base import APISub, APIResponse
from vng_api.types import MissileState


class MissileSub(APISub):

    async def get(self, pid: int, missile_id: str) -> APIResponse[MissileState]:
        """Get a probe missile preparation, flight or history

        :param pid: Probe ID
        :param missile_id: Missile ID
        """
        return await self.client.api_call('get', f'probe/{pid}/missiles/{missile_id}', None,
                                          lambda inp: MissileState.from_dict(inp['missile']))
