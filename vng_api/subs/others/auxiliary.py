from typing import List

from vng_api.base import APISub, APIResponse
from vng_api.helper.internal import build_url
from vng_api.types import ResourceAmounts
from vng_api.types.others import OthersAuxiliariesResponse, OthersAuxiliary, OthersDepotTransferAction, OthersDepotActionBase, OthersRepairAction, \
    OthersDeuteriumTransferAction


class AuxiliarySub(APISub):

    async def get_all(self, sid: str, cursor: str | None = None, limit: int | None = None) -> APIResponse[OthersAuxiliariesResponse]:
        """Get a cursor-paginated auxiliary page

        :param sid: Ship ID
        :param cursor: Pagination cursor
        :param limit: Page limit, min: 1, max: 500
        """
        url = build_url(f'others/ships/{sid}/auxiliaries', {'cursor': cursor, 'limit': limit})
        return await self.client.api_call('get', url, None, lambda x: OthersAuxiliariesResponse.from_dict(x))

    async def get(self, sid: str, auxiliary_id: str) -> APIResponse[OthersAuxiliary]:
        """Get one auxiliary

        :param sid: Ship ID
        :param auxiliary_id: Auxiliary ID
        """
        return await self.client.api_call('get', f'others/ships/{sid}/auxiliaries/{auxiliary_id}', None,
                                          lambda x: OthersAuxiliary.from_dict(x['auxiliary']))

    async def deposit(self, sid: str,
                      auxiliary_id: str,
                      depot_id: str,
                      resources: ResourceAmounts,
                      item_ids: List[str]) -> APIResponse[OthersDepotTransferAction]:
        """Start depot deposits

        :param sid: Ship ID
        :param auxiliary_id: Executing auxiliary ID
        :param depot_id: Target depot
        :param resources: Resources to deposit
        :param item_ids: Items to deposit
        """
        param = {
            'depotId': depot_id,
            'resources': resources.to_dict(),
            'itemIds': item_ids,
        }
        return await self.client.api_call('post', f'others/ships/{sid}/auxiliaries/{auxiliary_id}/depot-deposits', param,
                                          lambda x: OthersDepotTransferAction.from_dict(x['action']))

    async def withdraw(self,
                       sid: str,
                       auxiliary_id: str,
                       depot_id: str,
                       resources: ResourceAmounts,
                       item_ids: List[str]) -> APIResponse[OthersDepotTransferAction]:
        """Start depot withdrawal

        :param sid: Ship ID
        :param auxiliary_id: Executing auxiliary ID
        :param depot_id: Target depot
        :param resources: Resources to withdraw
        :param item_ids: Items to withdraw
        """
        param = {
            'depotId': depot_id,
            'resources': resources.to_dict(),
            'itemIds': item_ids,
        }
        return await self.client.api_call('post', f'others/ships/{sid}/auxiliaries/{auxiliary_id}/depot-withdrawals', param,
                                          lambda x: OthersDepotTransferAction.from_dict(x['action']))

    async def build_germination_depot(self, sid: str, auxiliary_id: str) -> APIResponse[OthersDepotActionBase]:
        """Build a germination depot

        An idle embarked auxiliary of an idle mothership reserves 2 ECE of metals and builds for 1800 seconds.
        Black-hole sectors are forbidden. Materials are lost on interruption. Each successful action creates one shared,
        indestructible, unlimited-capacity SQL depot. No client-supplied cost, duration or capacity is accepted.
        Successful completion also records the depot sector in the builder fleet's known depots,
        exposed by GET /api/others/fleets/{fleetId}/known-depots. Starting or interrupting construction
        does not record a discovery.

        :param sid: Ship ID
        :param auxiliary_id: Executing auxiliary ID
        """
        return await self.client.api_call('post', f'others/ships/{sid}/auxiliaries/{auxiliary_id}/build-germination-depot', None,
                                          lambda x: OthersDepotActionBase.from_dict(x['action']))

    async def repair(self, sid: str, auxiliary_id: str, percent: int) -> APIResponse[OthersRepairAction]:
        """Repair a ship with an embarked auxiliary

        Requires an owned active ship and a free embarked auxiliary belonging to it.
        integrityPercent counts whole integrity points, including on standard ships
        whose maximum is 20 (mothership maximum is 100). The requested amount is
        capped at missing integrity. Duration and metals use the same configuration
        as Manny repair: manny.actions.repairSecondsPerIntegrityPercent (default
        600 seconds per point) and manny.actions.repairMetalsPerIntegrityPercent
        (default 0.01 ECE per point). Available ship inventory metals are consumed
        immediately; reserved metals cannot be spent. The auxiliary remains busy
        until scheduled completion, which restores integrity up to max_integrity
        and releases the auxiliary. Other repairs may run concurrently; completion
        reports the points actually restored, without refunding an overlapping repair.
        An embarked repair continues during carrier movement. Ship destruction
        fails the action with carrier_destroyed without restoring integrity. Poll
        GET /api/others/actions/{actionId} for completion. The task is also available
        as repair through the atomic auxiliary task batch endpoint.

        :param sid: Ship ID
        :param auxiliary_id: Executing auxiliary ID
        :param percent: nr of percent to repair
        """
        return await self.client.api_call('post', f'others/ships/{sid}/auxiliaries/{auxiliary_id}/repair', {'integrityPercent': percent},
                                          lambda inp: OthersRepairAction.from_dict(inp['action']))

    async def transfer_deuterium(self, sid: str, auxiliary_id: str, target_ship_id: str, amount: float) -> APIResponse[OthersDeuteriumTransferAction]:
        """Schedule a tank-to-tank deuterium transfer

        :param sid: Ship ID
        :param auxiliary_id: Executing auxiliary ID
        :param target_ship_id: Target ship ID
        :param amount: amount to transfer
        """
        param = {
            'targetShipId': target_ship_id,
            'amount': amount,
        }
        return await self.client.api_call('post', f'others/ships/{sid}/auxiliaries/{auxiliary_id}/transfer-deuterium', param,
                                          lambda inp: OthersDeuteriumTransferAction.from_dict(inp['action']))
