from vng_api.base import APISub
from typing import TYPE_CHECKING

from vng_api.subs.others.fleet import OthersFleetSub
from vng_api.subs.others.ship import OthersShipSub
from vng_api.subs.others.sector import OthersSectorSub

if TYPE_CHECKING:
    from vng_api.client import APIClient


class OthersSub(APISub):

    def __init__(self, client: "APIClient"):
        super().__init__(client)
        self.fleet: OthersFleetSub = OthersFleetSub(client)
        self.ship: OthersShipSub = OthersShipSub(client)
        self.sector: OthersSectorSub = OthersSectorSub(client)
