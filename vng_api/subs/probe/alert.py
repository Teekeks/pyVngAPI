from typing import Literal

from vng_api.base import APISub, APIResponse
from vng_api.helper.internal import build_url
from vng_api.types import ProbeAlertResponse


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
