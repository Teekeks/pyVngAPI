from vng_api.base import APISub, APIResponse
from typing import TYPE_CHECKING

from vng_api.helper.internal import remove_none
from vng_api.subs.probe.damage_warning import DamageWarningSub
from vng_api.subs.probe.improvement import ImprovementSub
from vng_api.subs.probe.manny import MannySub
from vng_api.subs.probe.missile import MissileSub
from vng_api.subs.probe.scut_network import SCUTNetworkSub
from vng_api.subs.probe.sector import ProbeSectorSub
from vng_api.subs.probe.message import MessageSub
from vng_api.subs.probe.storage_container import StorageContainerSub
from vng_api.subs.probe.alert import AlertSub
from vng_api.types import ProbeType, OutOfRangeProbe, Probe, ProbeSummaryList, Vector, Movement

if TYPE_CHECKING:
    from vng_api.client import APIClient

__all__ = ['ProbeSub']


class ProbeSub(APISub):

    def __init__(self, client: "APIClient"):
        super().__init__(client)
        self.sector: ProbeSectorSub = ProbeSectorSub(client)
        self.missile: MissileSub = MissileSub(client)
        self.storage_container: StorageContainerSub = StorageContainerSub(client)
        self.alert: AlertSub = AlertSub(client)
        self.damage_warning: DamageWarningSub = DamageWarningSub(client)
        self.improvement: ImprovementSub = ImprovementSub(client)
        self.message: MessageSub = MessageSub(client)
        self.scut_network: SCUTNetworkSub = SCUTNetworkSub(client)
        self.manny: MannySub = MannySub(client)

    async def get(self, pid: int) -> APIResponse[ProbeType]:
        """Get a Neumann probe by id

        :param pid: Probe ID
        """
        return await self.client.api_call('get', f'probe/{pid}', None,
                                          lambda inp: OutOfRangeProbe.from_dict(inp['probe']) if inp['probe']['status'] == 'out_of_scut_range'
                                          else Probe.from_dict(inp['probe']))

    async def get_default(self) -> APIResponse[Probe]:
        """Get default Neumann probe"""
        return await self.client.api_call('get', 'probe', None,
                                          lambda inp: Probe.from_dict(inp['probe']))

    async def get_summary_list(self) -> APIResponse[ProbeSummaryList]:
        """List player Neumann Probes"""
        return await self.client.api_call('get', 'probes', None,
                                          lambda inp: ProbeSummaryList.from_dict(inp))

    async def update(self, pid: int, name: str | None = None, is_default: bool | None = None) -> APIResponse[ProbeSummaryList]:
        """Update a Neumann probe

        Renames the requested owned probe when `name` is provided. When `is_default` is True, sets the requested owned probe as the player's
        default probe. The current default probe and the requested probe must be in the same sector, or both sectors must be covered by the same
        active SCUT network, before the default probe can be changed.

        :param pid: Probe ID
        :param name: if set, changes the name of the Probe
        :param is_default: If set, changes the default probe to the specified one
        """
        body = remove_none({
            'name': name,
            'isDefault': is_default
        })
        ret = await self.client.api_call('patch', f'probe/{pid}', body, lambda inp: ProbeSummaryList.from_dict(inp))
        if ret.success:
            await self.client.issue_cache_update(ret.data)
        return ret

    async def move(self, pid: int, vector: Vector = None, x: int = None, y: int = None, z: int = None) -> APIResponse[Movement]:
        """Start an asynchronous intersector movement

        The probe must have at least 10 percent integrity when movement preparation starts. When the origin and destination each contain an
        active transit-beacon relay in the same SCUT network, the movement is protected from high-velocity destruction and its total intersector
        integrity loss is capped at 9 percentage points.

        If vector is passed, it will be prefered over x, y, z

        :param pid: Probe ID
        :param vector: Target vector of where to move to, either set this or x, y & z
        :param x: Target x coordinate
        :param y: Target y coordinate
        :param z: Target z coordinate
        :raises ValueError: if vector is None and at least one of x, y, z is also None"""
        if vector is not None:
            x, y, z = vector
        else:
            if x is None or y is None or z is None:
                raise ValueError('x and y and z or vector must be specified')
        payload = {'x': x, 'y': y, 'z': z}
        return await self.client.api_call('post', f'probe/{pid}/move', payload,
                                          lambda inp: Movement.from_dict(inp['movement']))

    async def cancel_move(self, pid: int) -> APIResponse[None]:
        """Cancel an asynchronous intersector movement

        :param pid: Probe ID"""
        return await self.client.api_call('delete', f'probe/{pid}/move')
