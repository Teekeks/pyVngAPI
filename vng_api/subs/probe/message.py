from typing import List, Literal

from vng_api.base import APISub, APIResponse
from vng_api.helper.internal import build_url
from vng_api.types import MessageResponse, Message


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

    async def send(self,
                   pid: int,
                   body: str,
                   recipient_id: int | str,
                   recipient_type: Literal['probe', 'planet'] = 'probe') -> APIResponse[Message]:
        """Send a message to a reachable probe or inhabited planet.

        Creates an unread message from the current probe to a recipient. Probe recipients must be in the exact same sector as the sender probe,
        or both probes must be inside coverage of the same active SCUT relay network. Planet recipients must be inhabited planets in the current
        sector. If the recipient type is omitted, `probe` is used. After completing an Oracle mission, sending a player's exact username to the
        Oracle planet whose mission has been completed by any player produces a planet-originated reply containing the approximate normalized
        direction vector and FCC distance to that player's default probe. A successful lookup starts a 24-hour cooldown shared by every visitor
        to that Oracle planet; unknown usernames do not consume it, while requests during the cooldown receive a polite refusal.

        :param pid: Probe ID
        :param body: The message to send, between 1 and 2000 characters long
        :param recipient_id: Probe id for `probe`, planet object id for `planet`.
        :param recipient_type: The type of recipient
        :raises ValueError: if `body` is not between 1 and 2000 characters long
        """
        if not (1 <= len(body) <= 2000):
            raise ValueError('Message body must be between 1 and 2000 characters long')
        param = {
            'recipient': {
                'id': recipient_id,
                'type': recipient_type
            },
            'body': body,
        }
        return await self.client.api_call('post', f'probe/{pid}/messages', param, lambda inp: Message.from_dict(inp['message']))
