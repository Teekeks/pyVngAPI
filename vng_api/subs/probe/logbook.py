from vng_api.base import APISub, APIResponse
from vng_api.helper.internal import build_url, remove_none
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

    async def add_page(self, pid: int, title: str, content: str) -> APIResponse[LogbookPage]:
        """Create a probe logbook page

        Creates a page in the selected probe's logbook.

        :param pid: Probe ID
        :param title: Title of the new page, between 1 and 120 characters
        :param content: Initial content of the page, up to 20_000 characters
        """
        param = {'title': title, 'content': content}
        return await self.client.api_call('post', f'probe/{pid}/logbook-page', param, lambda inp: LogbookPage.from_dict(inp['page']))

    async def delete(self, pid: int, page_id: int) -> APIResponse[None]:
        """Delete a probe logbook page

        :param pid: Probe ID
        :param page_id: Page ID
        """
        return await self.client.api_call('delete', f'/api/probe/{pid}/logbook-page/{page_id}', None, None)

    async def update(self, pid: int, page_id: int, title: str | None, content: str | None) -> APIResponse[LogbookPage]:
        """Update a probe logbook page

        :param pid: Probe ID
        :param page_id: Page ID
        :param title: New title, leave None if not intending to change
        :param content: new Content, leave None if not intenting to change
        :raises ValueError: If both title and content are None
        """
        body = remove_none({'title': title, 'content': content})
        if len(body.keys()) == 0:
            raise ValueError('Specify at least one of title and content')
        ret = await self.client.api_call('patch', f'/api/probe/{pid}/logbook-page/{page_id}', body, lambda inp: LogbookPage.from_dict(inp['page']))
        if ret.success:
            await self.client.issue_cache_update(ret.data)
        return ret

