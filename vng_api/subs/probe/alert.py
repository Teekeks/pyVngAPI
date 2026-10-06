from typing import Literal

from vng_api.base import APISub, APIResponse
from vng_api.helper.internal import build_url
from vng_api.types import ProbeAlertResponse, Alert, ProbeAlertsMarkAllReadResponse


class AlertSub(APISub):

    async def get_all(self, pid: int, status: Literal['unread'] | str | None = None) -> APIResponse[ProbeAlertResponse]:
        """List persistent probe alerts.

        Returns persistent alerts produced for the authenticated probe. Alerts currently cover fragile external storage movement warnings,
        intelligent-life detections when the probe arrives in a sector, instance-switch mind snapshot transfer notices, destroyed owned-probe
        notices, debug-injected sector object detections, and anomaly detections.

        :param pid: Probe ID
        :param status: Message Status to filter for
        """
        url = build_url(f'probe/{pid}/alerts', {'status': status})
        return await self.client.api_call('get', url, None, lambda inp: ProbeAlertResponse.from_dict(inp))

    async def read(self, pid: int, alert_id: float) -> APIResponse[Alert]:
        """Mark a persistent probe alert as read

        :param pid: Probe ID
        :param alert_id: Alert ID
        """
        data = await self.client.api_call('patch', f'probe/{pid}/alerts/{alert_id}', None,
                                          lambda inp: Alert.from_dict(inp['alert']))
        if data.success:
            await self.client.issue_cache_update(data.data)
        return data

    async def delete(self, pid: int, alert_id: str) -> APIResponse[None]:
        """Delete a persistent probe alert.

        Permanently deletes the alert only when it belongs to the selected probe owned by the authenticated player. An unknown alert or an alert
        belonging to another probe returns `404`.

        :param pid: Probe ID
        :param alert_id: Alert ID
        """
        return await self.client.api_call('delete', f'probe/{pid}/alerts/{alert_id}', None, None)

    async def read_all(self, pid: int) -> APIResponse[ProbeAlertsMarkAllReadResponse]:
        """Mark all persistent probe alerts as read

        Marks every unread persistent alert, of any type, as read for the selected owned probe. No request body is required.
        Already-read alerts keep their readAt and updatedAt timestamps. Returns the number of newly marked alerts, or zero when none are unread.
        Other probes and live sector warnings are unaffected.

        :param pid: Probe ID
        """
        return await self.client.api_call('post', f'probe/{pid}/alerts/mark-all-read', None,
                                          lambda inp: ProbeAlertsMarkAllReadResponse.from_dict(inp))
