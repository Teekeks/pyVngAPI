from typing import List

from vng_api.base import APISub, APIResponse
from vng_api.helper.internal import build_url
from vng_api.types import ProbeImprovement, ProbeImprovementBlueprintShareResponse


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

    async def share(self,
                    pid: int,
                    improvement_id: str,
                    recipient_id: int) -> APIResponse[ProbeImprovementBlueprintShareResponse]:
        """Share a known probe-improvement blueprint through SCUT

        Copies a blueprint known by the authenticated player to the player who owns the recipient probe. The sender and recipient probes must be
        covered by at least one common active SCUT network; merely occupying the same sector without SCUT coverage is insufficient. The sender
        keeps the blueprint, the recipient gains it for all owned probes, and the recipient probe receives one persistent `blueprint_shared` alert.
        Replaying the same share is idempotent and does not duplicate that alert. The `/scut` WebUI page exposes this operation for blueprints and
        recipient probes reachable through the selected network.

        :param pid: Probe ID
        :param improvement_id: ID of the improvement to share
        :param recipient_id: ID of the recipient probe
        """
        param = {'recipientProbeId': recipient_id}
        return await self.client.api_call('post', f'probe/{pid}/probe-improvement-blueprints/{improvement_id}/share', param,
                                          lambda inp: ProbeImprovementBlueprintShareResponse.from_dict(inp))
