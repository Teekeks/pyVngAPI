from typing import List

from vng_api.base import APISub, APIResponse
from vng_api.types import Vector
from vng_api.types.others import OthersFleet, OthersFleetSummary, OthersFleetMoveResponse, OthersDepotSummary


class OthersFleetSub(APISub):

    async def get(self, fid: str) -> APIResponse[OthersFleet]:
        """Get one owned fleet

        :param fid: Fleet ID
        """
        return await self.client.api_call('get', f'others/fleets/{fid}', None, lambda inp: OthersFleet.from_dict(inp['fleet']))

    async def get_summary_list(self) -> APIResponse[List[OthersFleetSummary]]:
        """List owned Others fleets"""
        return await self.client.api_call('get', 'others/fleets', None,
                                          lambda inp: [OthersFleetSummary.from_dict(x) for x in inp['fleets']])

    async def move(self, fid: str, target: Vector, leave_auxiliaries_behind: bool = False) -> APIResponse[OthersFleetMoveResponse]:
        """Schedule independent moves for eligible fleet ships.

        Each surviving fleet ship is evaluated independently against the same destination, relative to the owning player's home sector. The response
        always contains actions, ignored and blocked arrays, including empty arrays. A per-ship refusal does not cancel moves accepted for other ships.
        HTTP 202 may therefore contain no accepted actions, even when every ship is ignored or blocked. Destroyed ships are omitted.

        Accepted actions are queued for asynchronous execution. Use action.id with GET /api/others/actions/{actionId} to follow a move, or cancel it
        through DELETE /api/others/ships/{shipId}/move before cancelableUntil. endsAt is the planned arrival time, not the departure time.

        :param fid: Fleet ID
        :param target: The target system coordinates
        :param leave_auxiliaries_behind: if ture, leaves deployed auxiliaries behind
        """
        param = {
            'target': target.to_dict(),
            'leaveAuxiliariesBehind': leave_auxiliaries_behind
        }
        return await self.client.api_call('post', f'others/fleets/{fid}/move', param,
                                          lambda inp: OthersFleetMoveResponse.from_dict(inp))

    async def known_depots(self, fid: str) -> APIResponse[List[OthersDepotSummary]]:
        """List depot sectors discovered by one owned fleet.

        Returns all known germination depot sectors, ordered by x, y, then z.
        Coordinates are relative to the owning player's home. A sector is recorded when a ship of this fleet arrives there and at least one completed
        depot is present, regardless of its sealed, impacted or open state, or when an auxiliary of this fleet successfully completes construction of
        a depot. Queued, unfinished or interrupted constructions do not add discoveries. Multiple depots or arrivals in a sector produce a single
        entry. Knowledge persists after departure and is private to each fleet, including fleets with the same owner.
        Reading this endpoint does not discover depots. Existing visits and constructions are not backfilled; discovery starts with arrivals
        and successful construction completions after migration.

        :param fid: Fleet ID
        """
        return await self.client.api_call('get', f'others/fleets/{fid}/known-depots', None,
                                          lambda inp: [OthersDepotSummary.from_dict(x) for x in inp['knownDepots']])
