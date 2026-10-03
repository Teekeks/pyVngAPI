from typing import List

from vng_api.base import APISub, APIResponse
from vng_api.helper.internal import build_url
from vng_api.types import ResourceAmounts
from vng_api.types.others import OthersAuxiliariesResponse, OthersAuxiliary, OthersDepotTransferAction


class AuxiliarySub(APISub):

    async def get_all(self, sid: str, cursor: str | None = None, limit: int | None = None) -> APIResponse[OthersAuxiliariesResponse]:
        """Get a cursor-paginated auxiliary page

        :param sid: Ship ID
        :param cursor: Pagination cursor
        :param limit: Page limit, min: 1, max: 500
        """
        url = build_url(f'others/ships/{sid}/auxiliaries', {'cursor': cursor, 'limit': limit})
        return await self.client.api_call('get', url, None, lambda x: OthersAuxiliariesResponse.from_dict(x))

    async def get(self, sid: str, auxiliary_id: str) -> APIResponse[OthersAuxiliary]:
        """Get one auxiliary

        :param sid: Ship ID
        :param auxiliary_id: Auxiliary ID
        """
        return await self.client.api_call('get', f'others/ships/{sid}/auxiliaries/{auxiliary_id}', None,
                                          lambda x: OthersAuxiliary.from_dict(x['auxiliary']))

    async def deposit(self, sid: str,
                      auxiliary_id: str,
                      depot_id: str,
                      resources: ResourceAmounts,
                      item_ids: List[str]) -> APIResponse[OthersDepotTransferAction]:
        """Start depot deposits

        :param sid: Ship ID
        :param auxiliary_id: Executing auxiliary ID
        :param depot_id: Target deposit
        :param resources: Resources to deposit
        :param item_ids: Items to deposit
        """
        param = {
            'depotId': depot_id,
            'resources': resources.to_dict(),
            'itemIds': item_ids,
        }
        return await self.client.api_call('post', f'others/ships/{sid}/auxiliaries/{auxiliary_id}/depot-deposits', param,
                                          lambda x: OthersDepotTransferAction.from_dict(x['action']))
