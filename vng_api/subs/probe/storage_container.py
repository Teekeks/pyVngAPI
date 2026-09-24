from typing import List

from vng_api.base import APISub, APIResponse
from vng_api.types import StorageContainerInventoryResponse, StorageContainer


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
