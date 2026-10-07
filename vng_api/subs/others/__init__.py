from vng_api.base import APISub, APIResponse
from typing import TYPE_CHECKING

from vng_api.subs.others.fleet import OthersFleetSub
from vng_api.subs.others.ship import OthersShipSub
from vng_api.subs.others.sector import OthersSectorSub
from vng_api.types import MissileState
from vng_api.types.others import OthersOverview

if TYPE_CHECKING:
    from vng_api.client import APIClient


class OthersSub(APISub):

    def __init__(self, client: "APIClient"):
        super().__init__(client)
        self.fleet: OthersFleetSub = OthersFleetSub(client)
        self.ship: OthersShipSub = OthersShipSub(client)
        self.sector: OthersSectorSub = OthersSectorSub(client)

    async def overview(self) -> APIResponse[OthersOverview]:
        """Get the operator Others overview
        """
        return await self.client.api_call('get', 'others', None, lambda inp: OthersOverview.from_dict(inp['others']))

    async def get_missile(self, missile_id: str) -> APIResponse[MissileState]:
        """Get an owned missile launch or history

        Missile state without absolute coordinates

        :param missile_id: Missile ID
        """
        return await self.client.api_call('get', f'others/missiles/{missile_id}', None, lambda inp: MissileState.from_dict(inp['missile']))
