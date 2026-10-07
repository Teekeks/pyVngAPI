from typing import Literal, List

from vng_api.base import APISub, APIResponse
from vng_api.helper.internal import build_url
from vng_api.types.others import OthersAlert


class OthersAlertSub(APISub):

    async def get_all(self, status: Literal['unread'] | str | None = None) -> APIResponse[List[OthersAlert]]:
        """List persistent alerts for owned Others ships

        :param status: Message Status to filter for
        """
        url = build_url('others/alerts', {'status': status})
        return await self.client.api_call('get', url, None, lambda inp: [OthersAlert.from_dict(x) for x in inp['alerts']])

    async def read(self, alert_id: str) -> APIResponse[OthersAlert]:
        """Mark one owned Others alert as read

        :param alert_id: Alert ID
        """
        ret = await self.client.api_call('patch', f'others/alerts/{alert_id}', None, lambda inp: OthersAlert.from_dict(inp['alert']))
        if ret.success:
            await self.client.issue_cache_update(ret.data)
        return ret
