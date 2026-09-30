from vng_api.base import APISub, APIResponse
from vng_api.helper.internal import build_url
from vng_api.types.others import OthersAuxiliariesResponse


class AuxiliarySub(APISub):

    async def get_all(self, sid: str, cursor: str | None = None, limit: int | None = None) -> APIResponse[OthersAuxiliariesResponse]:
        """Get a cursor-paginated auxiliary page

        :param sid: Ship ID
        :param cursor: Pagination cursor
        :param limit: Page limit, min: 1, max: 500
        """
        url = build_url(f'others/ships/{sid}/auxiliaries', {'cursor': cursor, 'limit': limit})
        return await self.client.api_call('get', url, None, lambda x: OthersAuxiliariesResponse.from_dict(x))
