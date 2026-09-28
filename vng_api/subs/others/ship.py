from vng_api.base import APISub, APIResponse
from vng_api.types.others import OthersShip


class OthersShipSub(APISub):

    async def get(self, sid: str) -> APIResponse[OthersShip]:
        """Get one owned Others ship

        :param sid: Ship id"""
        return await self.client.api_call('get', f'others/ships/{sid}', None,
                                          lambda inp: OthersShip.from_dict(inp['ship']))
