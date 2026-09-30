from vng_api.base import APISub, APIResponse
from vng_api.types import ProbeDamageWarningResponse, Alert


class DamageWarningSub(APISub):

    async def get_all(self, pid: int) -> APIResponse[ProbeDamageWarningResponse]:
        """List probe movement damage warnings.

        Returns persistent warnings produced when a fragile chain of additional storage containers may lose one container during a sector movement.
        The starting threshold depends on probe model and completed improvements: 5 additional containers for a generic probe, 10 with
        reinforced couplings, 2 for a deuterium tanker, and 4 for a reinforced tanker. Risk starts at 10%, then adds 10 percentage points per extra
        container up to 100%. The warning exposes its effective threshold in `risk.ruleStartsAtAdditionalContainers`.

        :param pid: Probe ID
        """
        return await self.client.api_call('get', f'probe/{pid}/damage-warnings', None,
                                          lambda inp: ProbeDamageWarningResponse.from_dict(inp))

    async def read(self, pid: int, warning_id: str) -> APIResponse[Alert]:
        """Mark a movement damage warning as read

        :param pid: Probe ID
        :param warning_id: Warning ID
        """
        data = await self.client.api_call('patch', f'probe/{pid}/damage-warnings/{warning_id}', None,
                                          lambda inp: Alert.from_dict(inp['damageWarning']))
        if data.success:
            await self.client.issue_cache_update(data.data)
        return data

    async def delete(self, pid: int, warning_id: str) -> APIResponse[None]:
        """Delete a movement damage warning.

        Permanently deletes the warning only when it belongs to the selected probe owned by the authenticated player. An unknown warning or a
        warning belonging to another probe returns `404`.

        :param pid: Probe ID
        :param warning_id: Warning ID
        """
        return await self.client.api_call('delete', f'probe/{pid}/damage-warnings/{warning_id}', None, None)
