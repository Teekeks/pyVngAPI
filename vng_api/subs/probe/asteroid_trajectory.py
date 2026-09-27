from vng_api.base import APISub, APIResponse
from vng_api.types import AsteroidTrajectory


class AsteroidTrajectorySub(APISub):

    async def get(self, pid: int, trajectory_id: str) -> APIResponse[AsteroidTrajectory]:
        """Read locally detectable asteroid trajectory telemetry.

        Returns telemetry only while the selected probe occupies the trajectory's current sector. During deterministic stellar occultation
        windows the endpoint responds with 409 and no hidden trajectory data.

        :param pid: Probe ID
        :param trajectory_id:  Opaque trajectory id returned at launch.
        """
        return await self.client.api_call('get', f'/api/probe/{pid}/asteroid-trajectories/{trajectory_id}', None,
                                          lambda inp: AsteroidTrajectory.from_dict(inp['trajectory']))
