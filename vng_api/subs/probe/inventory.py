from vng_api.base import APISub, APIResponse
from vng_api.types import Item


class InventorySub(APISub):

    async def get_item(self, pid: int, item_id: str) -> APIResponse[Item]:
        """Get task state for an onboard inventory item

        :param pid: Probe ID
        :param item_id: Item ID
        """
        return await self.client.api_call('get', f'/api/probe/{pid}/inventory/{item_id}', None,
                                          lambda inp: Item.from_dict(inp['item']))
