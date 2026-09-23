from vng_api.base import APISub, APIResponse
from vng_api.types import ScutNetwork


class SCUTNetworkSub(APISub):

    async def get(self, pid: int, scut_id: int) -> APIResponse[ScutNetwork]:
        """Inspect a SCUT relay network covering the current probe

        :param pid: Probe ID
        :param scut_id: SCUT Network ID
        """
        return await self.client.api_call('get', f'probe/{pid}/scut-network/{scut_id}', None,
                                          lambda inp: ScutNetwork.from_dict(inp['network']))
