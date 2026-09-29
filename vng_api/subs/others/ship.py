from vng_api.base import APISub, APIResponse
from vng_api.types import Vector
from vng_api.types.others import OthersShip, OthersPlanetHarvestAction, OthersFleetMoveAcceptedAction


class OthersShipSub(APISub):

    async def get(self, sid: str) -> APIResponse[OthersShip]:
        """Get one owned Others ship

        :param sid: Ship id"""
        return await self.client.api_call('get', f'others/ships/{sid}', None,
                                          lambda inp: OthersShip.from_dict(inp['ship']))

    async def harvest(self, sid: str, target_id: str, auxiliary_count: int) -> APIResponse[OthersPlanetHarvestAction]:
        """Schedule a planetary swarm harvest.

        Reserves 2 ECE of inventory capacity per participating auxiliary. After the harvest consumes ten percent of every extracted resource, retained
        deuterium fills the coordinator ship tank first at the canonical rate of 100 tank points per ECE. Tank capacity already occupied or reserved
        by in-flight transfers is unavailable; any deuterium overflow is stored as an inventory resource. A terminal action result exposes the split
        in result.resources.deuteriumAllocation as tankPoints, tankEquivalentEce and inventoryEce.

        :param sid: Ship ID
        :param target_id: Target planet within same system
        :param auxiliary_count: number of auxiliaries to use
        """
        param = {
            'targetObjectId': target_id,
            'auxiliaryCount': auxiliary_count,
        }
        return await self.client.api_call('post', f'others/ships/{sid}/harvest', param,
                                          lambda x: OthersPlanetHarvestAction.from_dict(x['action']))

    async def move(self, sid: str, target: Vector, leave_auxiliaries_behind: bool = False) -> APIResponse[OthersFleetMoveAcceptedAction]:
        """Schedule an intersector move

        :param sid: Ship ID
        :param target: The target system coordinates
        :param leave_auxiliaries_behind: if ture, leaves deployed auxiliaries behind
        """
        param = {
            'target': target.to_dict(),
            'leaveAuxiliariesBehind': leave_auxiliaries_behind
        }
        return await self.client.api_call('post', f'others/ships/{sid}/move', param,
                                          lambda x: OthersFleetMoveAcceptedAction.from_dict(x['action']))
