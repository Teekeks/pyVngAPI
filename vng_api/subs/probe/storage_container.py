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
