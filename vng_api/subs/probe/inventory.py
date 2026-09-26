from vng_api.base import APISub, APIResponse
from vng_api.helper.internal import remove_none
from vng_api.types import Item, ProbeInventoryJettisonResponse


class InventorySub(APISub):

    async def get_item(self, pid: int, item_id: str) -> APIResponse[Item]:
        """Get task state for an onboard inventory item

        :param pid: Probe ID
        :param item_id: Item ID
        """
        return await self.client.api_call('get', f'/api/probe/{pid}/inventory/{item_id}', None,
                                          lambda inp: Item.from_dict(inp['item']))

    async def jettison(self,
                       pid: int,
                       item_id: str,
                       amount: int | float | None = None,
                       container_id: str | None = None) -> APIResponse[ProbeInventoryJettisonResponse]:
        """Jettison an inventory entry into space

        Discards stored metals/non-metal materials by amount, ejects an idle onboard Manny into the current sector, deploys a scut_relay item as an
        inactive SCUT relay in the current sector, or adds other supported crafted items to an aggregated drifting-item stack in the current sector.
        Non-persisted core equipment and additional containers cannot be jettisoned. The external deuterium tank is not jettisonable.

        :param pid: Probe ID
        :param item_id: Item ID
        :param amount: Amount to discard. For stored metals/non-metal materials this uses equivalent earth containers; for the deuterium tank this
            uses tank percentage points. Omit it to discard the full selected stock.
        :param container_id: Optional source container id for stored resource jettison.
        """
        param = remove_none({'amount': amount, 'containerId': container_id})
        ret = await self.client.api_call('post', f'/api/probe/{pid}/inventory/{item_id}/jettison', param,
                                         lambda inp: ProbeInventoryJettisonResponse.from_dict(inp))
        if ret.success:
            await self.client.issue_cache_update(ret.data.inventory)
            if ret.data.many is not None:
                await self.client.issue_cache_update(ret.data.many)
            if ret.data.jettisoned is not None:
                await self.client.issue_cache_update(ret.data.jettisoned)
        return ret
