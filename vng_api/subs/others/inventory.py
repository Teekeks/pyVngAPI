from typing import Literal, List

from vng_api.base import APISub, APIResponse
from vng_api.helper.internal import optional
from vng_api.types import ResourceType
from vng_api.types.others import OthersShipInventory, OthersInventoryTransferCreateResponse


class OthersShipInventorySub(APISub):

    async def get(self, sid: str) -> APIResponse[OthersShipInventory]:
        """Get this ship's own inventory

        :param sid: Ship ID
        """
        return await self.client.api_call('get', f'others/ships/{sid}/inventory', None,
                                          lambda x: OthersShipInventory.from_dict(x['inventory']))

    async def transfer(self,
                       sid: str,
                       auxiliary_id: str,
                       target_ship: str,
                       kind: Literal['item', 'resource'] | str,
                       item_ids: List[str] | None = None,
                       resource_type: ResourceType | None = None,
                       amount: float | None = None,) -> APIResponse[OthersInventoryTransferCreateResponse]:
        """Schedule an inventory transfer

        Uses an available auxiliary embarked on the source ship to transfer resources or inventory items to another owned ship in the same sector.
        The target inventory capacity and the transferred content are reserved until the scheduler completes the transfer.

        :param sid: Ship ID
        :param auxiliary_id: Acting auxiliary ID
        :param target_ship: target ship id
        :param kind: what to transfer
        :param item_ids: items to transfer
        :param resource_type: resource type to transfer
        :param amount: resource amout to transfer
        :raises ValueError: if kind is 'item' and item_ids is None
        :raises ValueError: if kind is 'resource' and resource_type or amount are None
        :raises ValueError: if kind is not 'item' or 'resource'
        """
        if kind not in ('item', 'resource'):
            raise ValueError(f'Invalid kind: {kind}')
        if kind == 'resource':
            if any([resource_type is None, amount is None]):
                raise ValueError('resource_type and amount need to be set for kind "resource"')
        else:
            if item_ids is None:
                raise ValueError('item_ids needs to be set for kind "item"')
        param = optional({
            'actorAuxiliaryId': auxiliary_id,
            'targetShipId': target_ship,
            'kind': kind,
            'itemIds': item_ids,
            'resourceType': resource_type,
            'amount': amount,
        }, ['itemIds', 'resourceType', 'amount'])
        return await self.client.api_call('post', f'others/ships/{sid}/inventory-transfers', param,
                                          lambda x: OthersInventoryTransferCreateResponse.from_dict(x))
