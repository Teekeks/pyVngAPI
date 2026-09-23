from typing import List

from vng_api.base import APISub, APIResponse
from vng_api.helper.internal import build_url
from vng_api.types import ProbeImprovement


class ImprovementSub(APISub):

    async def get_available(self, pid: int, include_all: bool | None = None) -> APIResponse[List[ProbeImprovement]]:
        """List available probe improvements.

        Returns probe improvements whose blueprints are known by the player owning the selected probe. The `done` flag is evaluated for that
        selected probe only. Pass `include_all=True` to include locked catalog entries as unavailable.

        :param pid: Probe ID
        :param include_all: Include locked improvements from the gameplay catalog.
        """
        url = build_url(f'probe/{pid}/probe-improvements-available', {'includeAll': include_all})
        return await self.client.api_call('get', url, None,
                                          lambda inp: [ProbeImprovement.from_dict(i) for i in inp['improvements']])
