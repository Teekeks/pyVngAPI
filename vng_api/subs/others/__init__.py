from vng_api.base import APISub, APIResponse
from typing import TYPE_CHECKING

from vng_api.helper.internal import build_url
from vng_api.subs.others.fleet import OthersFleetSub
from vng_api.subs.others.ship import OthersShipSub
from vng_api.subs.others.sector import OthersSectorSub
from vng_api.types import MissileState, SectorStorageInventory
from vng_api.types.others import OthersOverview, OthersInventoryTransfer, OthersCraft
from vng_api.subs.others.alert import OthersAlertSub

if TYPE_CHECKING:
    from vng_api.client import APIClient


class OthersSub(APISub):

    def __init__(self, client: "APIClient"):
        super().__init__(client)
        self.fleet: OthersFleetSub = OthersFleetSub(client)
        self.ship: OthersShipSub = OthersShipSub(client)
        self.sector: OthersSectorSub = OthersSectorSub(client)
        self.alert: OthersAlertSub = OthersAlertSub(client)

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

    async def get_depot(self, depot_id: str, limit: int = None, cursor: str = None) -> APIResponse[SectorStorageInventory]:
        """Read shared depot contents

        :param depot_id: Depot ID
        :param limit: Page limit. Default: 100, Max: 500, Min 1
        :param cursor: Pagination Cursor
        """
        url = build_url(f'others/germination-depots/{depot_id}/inventory', {'limit': limit, 'cursor': cursor})
        return await self.client.api_call('get', url, None, lambda inp: SectorStorageInventory.from_dict(inp))

    async def get_transfer(self, transfer_id: str) -> APIResponse[OthersInventoryTransfer]:
        """Get a transfer

        :param transfer_id: Transfer ID
        """
        return await self.client.api_call('get', f'others/inventory-transfers/{transfer_id}', None,
                                          lambda inp: OthersInventoryTransfer.from_dict(inp['transfer']))

    async def get_craft(self, craft_id: str) -> APIResponse[OthersCraft]:
        """Get one craft

        :param craft_id: Craft ID
        """
        return await self.client.api_call('get', f'others/crafts/{craft_id}', None,
                                          lambda inp: OthersCraft.from_dict(inp['craft']))
