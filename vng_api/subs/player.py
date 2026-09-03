from vng_api.base import APISub, APIResponse
from vng_api.types import Player, APIKey


class PlayerSub(APISub):

    async def get(self) -> APIResponse[Player]:
        """Get authenticated player"""
        return await self.client.api_call('get', 'me', None,
                                          lambda inp: Player.from_dict(inp['player']))

    async def create_api_key(self) -> APIResponse[APIKey]:
        """Create an API key for the authenticated player"""
        return await self.client.api_call('post', 'key', None,
                                          lambda inp: APIKey.from_dict(inp['apiKey']))
