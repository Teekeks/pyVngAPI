from typing import List, Literal

from vng_api.base import APISub, APIResponse
from vng_api.helper.internal import build_url
from vng_api.types import MessageResponse


class MessageSub(APISub):

    async def get_all(self,
                      pid: int,
                      limit: int | None = None,
                      offset: int | None = None,
                      status: Literal['unread'] | None = None) -> APIResponse[MessageResponse]:
        """List messages received by the current probe.

        Returns messages where the authenticated player's probe is the recipient. Messages are sorted newest first, include their read
        status, and are limited to the 50 latest messages by default.

        :param pid: Probe ID
        :param limit: Maximum number of messages to return. Default: 50, Min: 1, Max: 200
        :param offset: Number of newest messages to skip before returning the page. Default: 0
        :param status: Set to `unread` to return only unread received messages.
        """
        url = build_url(f'probe/{pid}/messages', {'limit': limit, 'offset': offset, 'status': status})
        return await self.client.api_call('get', url, None, lambda inp: MessageResponse.from_dict(inp))
