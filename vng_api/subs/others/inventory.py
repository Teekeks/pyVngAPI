from vng_api.base import APISub, APIResponse
from vng_api.types.others import OthersShipInventory


class OthersShipInventorySub(APISub):

    async def get(self, sid: str) -> APIResponse[OthersShipInventory]:
        """Get this ship's own inventory

        :param sid: Ship ID
        """
        return await self.client.api_call('get', f'others/ships/{sid}/inventory', None,
                                          lambda x: OthersShipInventory.from_dict(x['inventory']))
