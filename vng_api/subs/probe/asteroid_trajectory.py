from typing import Literal

from vng_api.base import APISub, APIResponse
from vng_api.helper.internal import remove_none
from vng_api.types import AsteroidTrajectory, Vector


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

    async def launch(self,
                     pid: int,
                     asteroid_id: str,
                     mode: Literal['system_impact', 'sector_transfer'],
                     target_id: str | None = None,
                     target_speed_c: float | None = None,
                     target: Vector | None = None,) -> APIResponse[AsteroidTrajectory]:
        """Launch a full motorized asteroid.

        Consumes the asteroid's binary fuel tank and creates one durable, scheduler-driven trajectory. A system impact accelerates around the
        sector reference star before a ten-minute coasting phase. A sector transfer accepts only a direct FCC-grid neighbor expressed in the
        player's relative frame; that neighbor sets a straight-line direction, and the asteroid then crosses one sector every 24 hours. Capture is
        guaranteed in the first entered sector containing at least one eligible body. In a stellar system the captor is selected proportionally to
        mass, so the star is overwhelmingly favored and places the asteroid in orbit when selected. Each sector crossed without an eligible body, and
        each failed capture attempt, reduces the next capture probability by 10 percentage points (100%, 90%, 80%, and so on). Crossing several
        empty sectors therefore makes a later capture progressively less certain. Black holes always capture the asteroid. Starting either
        trajectory mode interrupts every Manny mining into a container attached to the asteroid, including Mannys belonging to another probe, and
        sends them back with reason `target_container_departed_with_asteroid`. Absolute coordinates are never returned.

        :param pid: Probe ID
        :param asteroid_id: Asteroid ID
        :param mode: Travel Mode
        :param target_id: ID of target object within sector. for mode `system_impact`
        :param target_speed_c: Target speed of asteroid. for mode `system_impact`
        :param target: Target system. for mode `sector_transfer`
        """
        param = remove_none({
            'mode': mode,
            'targetObjectId': target_id,
            'targetSpeedC': target_speed_c,
            'target': target.to_dict() if target is not None else None,
        })
        return await self.client.api_call('post', f'/api/probe/{pid}/asteroids/{asteroid_id}/trajectories', param,
                                          lambda inp: AsteroidTrajectory.from_dict(inp['trajectory']))

