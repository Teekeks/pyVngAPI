from vng_api.base import APISub, APIResponse
from vng_api.types import LogbookPage


class LogBookSub(APISub):

    async def get(self, pid: int, page_id: int) -> APIResponse[LogbookPage]:
        """Get a probe logbook page

        :param pid: Probe ID
        :param page_id: Page ID
        """
        return await self.client.api_call('get', f'probe/{pid}/logbook-page/{page_id}', None,
                                          lambda inp: LogbookPage.from_dict(inp['page']))
