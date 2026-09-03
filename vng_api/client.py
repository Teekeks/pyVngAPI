import asyncio
from typing import Dict, Literal, Callable, Any, List
from datetime import datetime, UTC, timedelta
import aiohttp
import orjson

from vng_api.base import APIStats, BASEURL, APIResponse
from vng_api import __version__
from vng_api.subs.probe import ProbeSub
from vng_api.subs.sector import SectorSub
from vng_api.subs.player import PlayerSub

__all__ = ['APIClient']

from vng_api.types import CraftingRecipe


class APIClient:

    def __init__(self, token: str):
        self.stats: APIStats = APIStats()
        self.token = token
        # subs:
        self.sector: SectorSub = SectorSub(self)
        self.player: PlayerSub = PlayerSub(self)
        self.probe: ProbeSub = ProbeSub(self)

    def get_headers(self) -> Dict[str, str]:
        return {
            'Authorization': f'Bearer {self.token}',
            'User-Agent': f'VNG-API Client v{__version__} by Teekeks'
        }

    async def issue_cache_update(self, d: Any):
        # FIXME: implement
        pass

    async def api_call[T](self,
                          method: Literal['get', 'put', 'delete', 'post', 'patch'],
                          path: str,
                          json_data: Any | None = None,
                          data_transform: Callable[[Dict[Any, Any]], T] | None = None) -> APIResponse[T]:
        """Makes a call to the API using the given method.

        :param method: The HTTP method to use.
        :param path: The URL path excluding the base api path.
        :param json_data: The data to send as JSON.
        :param data_transform: A Function that transforms the api response"""
        async with aiohttp.ClientSession(headers=self.get_headers(),
                                         json_serialize_bytes=orjson.dumps) as session:
            ret = await session.request(method, BASEURL + path, json=json_data)
            error_code = error_message = data = None
            self.stats.update_from_response(ret)
            match ret.status:
                case 200 | 201:
                    raw_data = await ret.json()
                    data = data_transform(raw_data) if data_transform is not None else raw_data
                    success = True
                case 429:
                    unlock_at = datetime.now(UTC) + timedelta(seconds=self.stats.retry_after or 10)
                    while datetime.now(UTC) < unlock_at:
                        self.stats.retry_after = int((unlock_at - datetime.now(UTC)).total_seconds())
                        await asyncio.sleep(0.2)
                    return await self.api_call(method, path, json_data, data_transform)
                case 400 | 401 | 403 | 404 | 409 | 422:
                    success = False
                    raw_data = await ret.json()
                    error_message = raw_data.get('message')
                    error_code = raw_data.get('code')
                case 500 | 503:
                    success = False
                    error_message = await ret.text()
                    error_code = 'server_error'
                case _:
                    success = False
                    error_code = 'unknown_error'
                    error_message = ''
            return APIResponse(
                success=success,
                status=ret.status,
                error_message=error_message,
                error_code=error_code,
                data=data,
            )

    async def version(self) -> APIResponse[int]:
        """Get API Version"""
        return await self.api_call('get', 'version', None, lambda inp: inp['apiVersion'])

    async def crafting_recipes(self) -> APIResponse[List[CraftingRecipe]]:
        """List available crafting recipes"""
        return await self.api_call('get',
                                   'crafting-recipes',
                                   None,
                                   lambda inp: [CraftingRecipe.from_dict(d) for d in inp['recipes']])
