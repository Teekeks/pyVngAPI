from typing import List

from vng_api.base import APISub, APIResponse
from vng_api.types import StorageContainerInventoryResponse, StorageContainer, StorageContainerRules, CraftingReservationResponse


class StorageContainerSub(APISub):

    async def get(self, pid: int, container_id: str) -> APIResponse[StorageContainerInventoryResponse]:
        """Get one storage container content

        :param pid: Probe ID
        :param container_id: Container ID
        """
        return await self.client.api_call('get', f'probe/{pid}/storage-containers/{container_id}', None,
                                          lambda inp: StorageContainerInventoryResponse.from_dict(inp))

    async def get_all(self, pid: int) -> APIResponse[List[StorageContainer]]:
        """List probe storage containers.

        Returns the selected probe core storage and each additional container created from an additional_container inventory item. The deuterium tank
        is not managed here.

        :param pid: Probe ID
        """
        return await self.client.api_call('get', f'/api/probe/{pid}/storage-containers', None,
                                          lambda inp: [StorageContainer.from_dict(c) for c in inp['containers']])

    async def rename(self, pid: int, container_id: str, label: str) -> APIResponse[StorageContainerInventoryResponse]:
        """Rename a storage container

        :param pid: Probe ID
        :param container_id: Container ID
        :param label: The new label for the container
        """
        return await self.client.api_call('patch', f'probe/{pid}/storage-containers/{container_id}',
                                          {'label': label}, lambda inp: StorageContainerInventoryResponse.from_dict(inp))

    async def set_rules(self, pid: int, container_id: str, rules: StorageContainerRules) -> APIResponse[StorageContainerInventoryResponse]:
        """Update storage routing rules for a container.

        Priority routes matching new items to this selected-probe container first unless it is full. Exclusion avoids this container unless no
        other non-strict container can accept the item. Strict exclusion prevents automatic placement into this container.

        :param pid: Probe ID
        :param container_id: Container ID
        :param rules: New rules
        """
        return await self.client.api_call('patch', f'/api/probe/{pid}/storage-containers/{container_id}/rules', rules.to_dict(),
                                          lambda inp: StorageContainerInventoryResponse.from_dict(inp))

    async def reassign_crafting_reservation(self, pid: int, container_id: str) -> APIResponse[CraftingReservationResponse]:
        """Reassign active crafting reservations from a storage container.

        Atomically moves every active Manny or atomic-printer crafting output reservation targeting this container to other containers attached to
        the selected probe. Destination routing honors capacity and strict exclusion filters. If all reservations cannot be reassigned, none is
        changed.

        :param pid: Probe ID
        :param container_id: Container ID
        """
        return await self.client.api_call('post', f'/api/probe/{pid}/storage-containers/{container_id}/crafting-reservations/reassign',
                                          None, lambda inp: CraftingReservationResponse.from_dict(inp))
