from vng_api.base import APISub, APIResponse
from vng_api.types import StorageContainerInventoryResponse


class StorageContainerSub(APISub):

    async def get(self, pid: int, container_id: str) -> APIResponse[StorageContainerInventoryResponse]:
        """Get one storage container content

        :param pid: Probe ID
        :param container_id: Container ID
        """
        return await self.client.api_call('get', f'probe/{pid}/storage-containers/{container_id}', None,
                                          lambda inp: StorageContainerInventoryResponse.from_dict(inp))

    async def rename(self, pid: int, container_id: str, label: str) -> APIResponse[StorageContainerInventoryResponse]:
        """Rename a storage container

        :param pid: Probe ID
        :param container_id: Container ID
        :param label: The new label for the container
        """
        return await self.client.api_call('patch', f'probe/{pid}/storage-containers/{container_id}',
                                          {'label': label}, lambda inp: StorageContainerInventoryResponse.from_dict(inp))
