from typing import Literal, List

from vng_api.base import APISub, APIResponse
from vng_api.helper.internal import remove_none
from vng_api.types import Item, ProbeInventoryJettisonResponse, ResourceType, StorageMoveResponse


class InventorySub(APISub):

    async def get_item(self, pid: int, item_id: str) -> APIResponse[Item]:
        """Get task state for an onboard inventory item

        :param pid: Probe ID
        :param item_id: Item ID
        """
        return await self.client.api_call('get', f'probe/{pid}/inventory/{item_id}', None,
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
        ret = await self.client.api_call('post', f'probe/{pid}/inventory/{item_id}/jettison', param,
                                         lambda inp: ProbeInventoryJettisonResponse.from_dict(inp))
        if ret.success:
            await self.client.issue_cache_update(ret.data.inventory)
            if ret.data.many is not None:
                await self.client.issue_cache_update(ret.data.many)
            if ret.data.jettisoned is not None:
                await self.client.issue_cache_update(ret.data.jettisoned)
        return ret

    async def move(self,
                   pid: int,
                   actor_mid: str,
                   kind: Literal['resource', 'item', 'manny'],
                   to_container_id: str,
                   from_container_id: str | None = None,
                   resource_type: ResourceType | None = None,
                   amount: float | None = None,
                   item_id: str | None = None,
                   item_ids: List[str] | None = None,
                   target_mid: str | None = None,
                   target_mids: List[str] | None = None,
                   quantity: int | None = None,) -> APIResponse[StorageMoveResponse]:
        """Assign a Manny to move stock between containers.

        Starts a moving_stockage task on an idle onboard Manny. Unit items take 10 seconds; resources take 10 seconds per 0.05 ECE. Destination free
        capacity is evaluated after subtracting cargo already reserved by other active storage moves toward the same container. additional_container
        items cannot be moved through this endpoint; while onboard, they remain linked to the probe internal storage.

        :param pid: Probe ID
        :param actor_mid: ID of Idle onboard Manny that will perform the move.
        :param kind: The Kind of thing to move
        :param to_container_id: Target Container ID
        :param from_container_id: Required for resource moves.
        :param resource_type: The resource to move, Required for resource moves
        :param amount: Required for resource moves, in ECE.
        :param item_id: Single item id for item moves. Use itemIds for batch moves. additional_container items are rejected.
        :param item_ids: Multiple item ids for batch item moves. additional_container items are rejected.
        :param target_mid: Single Manny id for Manny moves. Use targetMannyIds for batch moves.
        :param target_mids: Multiple Manny ids for batch Manny storage moves.
        :param quantity: Optional cap applied to item_ids or target_mids.
        """
        data = remove_none({
            'actorMannyId': actor_mid,
            'kind': kind,
            'toContainerId': to_container_id,
            'fromContainerId': from_container_id,
            'resourceType': resource_type,
            'amount': amount,
            'itemId': item_id,
            'itemIds': item_ids,
            'targetMannyId': target_mid,
            'targetMannyIds': target_mids,
            'quantity': quantity,
        })
        ret = await self.client.api_call('post', f'probe/{pid}/storage-moves', data, lambda inp: StorageMoveResponse.from_dict(inp))
        if ret.success:
            await self.client.issue_cache_update(ret.data.inventory)
            await self.client.issue_cache_update(ret.data.manny)
        return ret
