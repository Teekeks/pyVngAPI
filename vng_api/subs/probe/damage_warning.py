from vng_api.base import APISub, APIResponse
from vng_api.types import ProbeDamageWarningResponse


class DamageWarningSub(APISub):

    async def get_all(self, pid: int) -> APIResponse[ProbeDamageWarningResponse]:
        """List probe movement damage warnings.

        Returns persistent warnings produced when a fragile chain of additional storage containers may lose one container during a sector movement.
        The starting threshold depends on probe model and completed improvements: 5 additional containers for a generic probe, 10 with
        reinforced couplings, 2 for a deuterium tanker, and 4 for a reinforced tanker. Risk starts at 10%, then adds 10 percentage points per extra
        container up to 100%. The warning exposes its effective threshold in `risk.ruleStartsAtAdditionalContainers`.

        :param pid: Probe ID
        """
        return await self.client.api_call('get', f'/api/probe/{pid}/damage-warnings', None,
                                          lambda inp: ProbeDamageWarningResponse.from_dict(inp))
