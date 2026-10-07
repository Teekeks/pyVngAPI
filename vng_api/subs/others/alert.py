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

    async def read_batch(self, alert_ids: List[str]) -> APIResponse[List[OthersAlert]]:
        """Mark a batch of owned Others alerts as read

        Marks only the supplied alerts as read, atomically. All alerts must belong to the authenticated account; an unknown or foreign identifier
        rejects the entire batch with 404 others_alert_not_found. Already-read alerts are accepted without changing their timestamps, so retries are
        safe. Returns the alerts in request order. Requires Others control permission and counts as one request against the normal per-token
        rate limit.

        :param alert_ids: Alert IDs
        """
        ret = await self.client.api_call('post', 'others/alerts/mark-read', {'alertIds': alert_ids},
                                         lambda inp: [OthersAlert.from_dict(x) for x in inp['alerts']])
        if ret.success:
            for alert in ret.data:
                await self.client.issue_cache_update(alert)
        return ret
