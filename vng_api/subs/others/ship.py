from typing import List, TYPE_CHECKING

from vng_api.base import APISub, APIResponse
from vng_api.types import Vector
from vng_api.types.others import OthersShip, OthersPlanetHarvestAction, OthersFleetMoveAcceptedAction, OthersCraft, OthersCraftResponse, \
    OthersLaserLockAction, OthersMissileLaunchResponse
from vng_api.subs.others.auxiliary import AuxiliarySub
from vng_api.subs.others.inventory import OthersShipInventorySub


if TYPE_CHECKING:
    from vng_api.client import APIClient


class OthersShipSub(APISub):

    def __init__(self, client: "APIClient"):
        super().__init__(client)
        self.auxiliary: AuxiliarySub = AuxiliarySub(client)
        self.inventory: OthersShipInventorySub = OthersShipInventorySub(client)

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

    async def cancel_harvest(self, sid: str) -> APIResponse[OthersPlanetHarvestAction]:
        """Interrupt and recall the harvest swarm

        :param sid: Ship ID
        """
        return await self.client.api_call('delete', f'others/ships/{sid}/harves', None,
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

    async def cancel_move(self, sid: str) -> APIResponse[OthersFleetMoveAcceptedAction]:
        """Request cancellation during the fifteen-minute window

        :param sid: Ship ID
        """
        return await self.client.api_call('delete', f'others/ships/{sid}/move', None,
                                          lambda x: OthersFleetMoveAcceptedAction.from_dict(x['action']))

    async def active_crafts(self, sid: str) -> APIResponse[List[OthersCraft]]:
        """List this mothership's crafts.

        Returns a crafts collection with recipeId, status, actionId and endsAt when scheduled. To count ongoing ship construction, select
        recipeId standard_ship and status queued or running. Read this state again after restarting a controller; terminal crafts do not occupy an
        active construction slot.

        :param sid: Ship ID
        """
        return await self.client.api_call('get', f'others/ships/{sid}/crafts', None,
                                          lambda inp: [OthersCraft.from_dict(x) for x in inp['crafts']])

    async def craft(self, sid: str, recipe_id: str, auxiliary_id: str) -> APIResponse[OthersCraftResponse]:
        """Schedule a mothership craft.

        Requires an owned mothership and an available embarked assistant auxiliary. Ingredients are consumed from unreserved inventory resources
        at acceptance, including inventory deuterium rather than propulsion fuel. The assistant stays busy until completion. Read canonical costs
        and durations from GET /api/others/crafting/recipes.

        standard_ship takes 604800 seconds (seven days) and consumes 6000 ECE of metals, 1000 of ice, 2000 of carbon_compounds and 100 of deuterium.
        On completion it creates a standard ship in the mothership's fleet and current sector, with one auxiliary and an empty 50-point fuel tank.
        The action result exposes output.kind and output.id. Several crafts can run concurrently using distinct assistants; any reconstruction
        reserve or three-construction limit is a controller policy, not an API restriction.

        :param sid: Ship ID
        :param recipe_id: Id of target recipe
        :param auxiliary_id: ID of auxiliary to use for craft
        """
        param = {
            'recipeId': recipe_id,
            'assistantAuxiliaryId': auxiliary_id
        }
        return await self.client.api_call('post', f'others/ships/{sid}/crafts', param, lambda inp: OthersCraftResponse.from_dict(inp))

    async def laser_lock(self, sid: str, target_id: str) -> APIResponse[OthersLaserLockAction]:
        """Schedule an immediate local laser lock

        :param sid: Ship ID
        :param target_id: Target ID
        """
        param = {'targetId': target_id}
        return await self.client.api_call('post', f'others/ships/{sid}/weapons/laser', param,
                                          lambda inp: OthersLaserLockAction.from_dict(inp['action']))

    async def inginte_missile(self, sid: str, missile_id: str, target_id: str) -> APIResponse[OthersMissileLaunchResponse]:
        """Schedule an immediate Others missile launch.

        targetId may identify a moving missile in the firing ship's current sector to attempt an interception. Each request launches one inventory
        missile at the selected target.

        :param sid: Ship ID
        :param missile_id: Missile ID
        :param target_id: Target ID
        """
        param = {
            'missileItemId': missile_id,
            'targetId': target_id
        }
        return await self.client.api_call('post', f'others/ships/{sid}/missile', param,
                                          lambda x: OthersMissileLaunchResponse.from_dict(x))
