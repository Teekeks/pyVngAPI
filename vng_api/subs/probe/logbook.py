from vng_api.base import APISub, APIResponse
from vng_api.helper.internal import build_url
from vng_api.types import LogbookPage, ProbeLogbookPagesResponse


class LogBookSub(APISub):

    async def get(self, pid: int, page_id: int) -> APIResponse[LogbookPage]:
        """Get a probe logbook page

        :param pid: Probe ID
        :param page_id: Page ID
        """
        return await self.client.api_call('get', f'probe/{pid}/logbook-page/{page_id}', None,
                                          lambda inp: LogbookPage.from_dict(inp['page']))

    async def get_all(self, pid: int, offset: int | None = None, limit: int | None = None) -> APIResponse[ProbeLogbookPagesResponse]:
        """List probe logbook pages

        Returns the selected probe's logbook pages, sorted by probe-local order. The default page size is 10 entries; use `limit` and `offset`
        to retrieve more.

        :param pid: Probe ID
        :param offset: Number of logbook pages to skip before returning the page.
        :param limit: Maximum number of logbook pages to return. Defaults to 10.
        """
        url = build_url(f'/api/probe/{pid}/logbook-pages', {'offset': offset, 'limit': limit})
        return await self.client.api_call('get', url, lambda inp: ProbeLogbookPagesResponse.from_dict(inp))
