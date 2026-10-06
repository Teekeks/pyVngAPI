from vng_api.helper.internal import optional, remove_none
from vng_api.base import APISub, APIBatchResult, APIResponse
from typing import TYPE_CHECKING, List, Dict, Any, Iterable, Literal

from vng_api.types import Manny, Printable, PrintResponse, ResourceType

if TYPE_CHECKING:
    from vng_api.client import APIClient

__all__ = ['MannyTaskManager', 'MannySub']


class MannyTaskManager(APISub):

    def __init__(self, client: "APIClient", pid: int):
        super().__init__(client)
        self.tasks: List[Dict[str, Any]] = []
        self.pid: int = pid
        self.results: APIBatchResult | None = APIBatchResult()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._check_run(True)

    async def _check_run(self, final: bool = False):
        if (len(self.tasks) == 0) or (not final and len(self.tasks) < 100):
            return
        ret = await self.client.api_call('post',
                                         f'probe/{self.pid}/mannies/tasks',
                                         {'tasks': self.tasks},
                                         lambda inp: [{
                                             'manny': Manny.from_dict(result['manny']) if result.get('manny') else None,
                                             'inventory': None,  # FIXME
                                             'improvements': None,  # FIXME
                                         } for result in inp['results']])
        if ret.success:
            for m in ret.data:
                if m['manny'] is not None:
                    await self.client.issue_cache_update(m['manny'])
        self.results.responses.append(ret)
        self.tasks = []

    async def _add_task(self, mid: str, task: str, payload: Dict[Any, Any]):
        self.tasks.append({
            'mannyId': mid,
            'task': task,
            'payload': payload,
        })
        await self._check_run()

    async def repair(self, mid: str, integrity: int):
        await self._add_task(mid, 'repair', {'integrityPercent': integrity})

    async def mine(self,
                   mid: str,
                   target_id: str,
                   resources: Iterable[ResourceType],
                   target_amount: float,
                   target_container: str | None = None):
        payload = optional({
             'objectId': target_id,
             'resources': resources,
             'targetAmount': target_amount,
             'targetContainer': target_container,
        }, ('targetContainer',))
        await self._add_task(mid, 'mine', payload)

    async def motorize_asteroid(self, mid: str, target_id: str):
        await self._add_task(mid, 'motorize-asteroid', {'objectId': target_id})

    async def refuel_motorized_asteroid(self, mid: str, target_id: str):
        await self._add_task(mid, 'refuel-motorized-asteroid', {'objectId': target_id})

    async def sculpt_duck_asteroid(self, mid: str, target_id: str):
        await self._add_task(mid, 'sculpt-duck-asteroid', {'objectId': target_id})

    async def craft(self, mid: str, recipe: str):
        await self._add_task(mid, 'craft', {'recipe': recipe})

    async def improve_probe(self, mid: str, improvement: str):
        await self._add_task(mid, 'improve-probe', {'improvement': improvement})

    async def assemble_probe(self, mid: str, model: Literal['generic', 'deuterium_tanker'], container_ids: Iterable[str]):
        await self._add_task(mid, 'assemble-probe', {'model': model, 'containerIds': list(container_ids)})

    async def salvage(self, mid: str, target_id: str):
        await self._add_task(mid, 'salvage', {'objectId': target_id})

    async def detach_storage_container(self,
                                       mid: str,
                                       container_id: str,
                                       mode: Literal['drifting', 'hidden_on_asteroid', 'attach_to_probe', 'hidden_on_dormant_construct'] = 'drifting',
                                       target_id: str | int | None = None):
        payload = optional({
            'containerId': container_id,
            'mode': mode,
            'objectId': target_id,
        }, ('objectId',))
        await self._add_task(mid, 'detach-storage-container', payload)

    async def drop_storage_container(self, mid: str, container_id: str, planet_id: str):
        await self._add_task(mid, 'drop-storage-container', {'containerId': container_id, 'planetId': planet_id})

    async def inspect_sector_object(self, mid: str, target_id: str):
        await self._add_task(mid, 'inspect-sector-object', {'objectId': target_id})

    async def recover_storage_container(self, mid: str, container_id: str):
        await self._add_task(mid, 'recover-storage-container', {'objectId': container_id})

    async def install_bookmark(self, mid: str, target_id: str, name: str):
        await self._add_task(mid, 'install-bookmark', {'name': name, 'objectId': target_id})

    async def recall(self, mid: str):
        await self._add_task(mid, 'recall', {})

    async def drop_manny_cargo(self, mid: str):
        await self._add_task(mid, 'drop-manny-cargo', {})

    async def refill_deuterium_tank(self, mid: str):
        await self._add_task(mid, 'refill-deuterium-tank', {})

    async def transfer_deuterium_to_probe(self, mid: str, target_id: int, amount: float):
        await self._add_task(mid, 'transfer-deuterium-to-probe', {'amount': amount, 'targetProbeId': target_id})

    async def transfer_to_probe(self, mid: str, target_id: int):
        await self._add_task(mid, 'transfer-to-probe', {'targetProbeId': target_id})

    async def turn_on_relay(self, mid: str, relay_id: int, network_name: str | None = None):
        payload = optional({
            'relayId': relay_id,
            'networkName': network_name
        }, ('networkName',))
        await self._add_task(mid, 'turn-on-relay', payload)

    async def install_scut_transit_beacon(self, mid: str, relay_id: int):
        """Starts a five-minute Manny task that equips an active SCUT relay in the probe current sector with a scut_transit_beacon.
        The task consumes one scut_transit_beacon item from the probe inventory.

        :param mid: The ID of the manny to carry out the task
        :param relay_id: The relay ID"""
        await self._add_task(mid, 'install-scut-transit-beacon', {'relayId': relay_id})

    async def ignite_missile(self, mid: str, target_id: str, missile_item_id: str | None = None):
        """Starts a one-minute missile preparation with the selected embarked Manny.
        When missileItemId is omitted, the first available missile in the probe inventory is used.

        :param mid: The ID of the manny to carry out the task
        :param target_id: The ID of the target to fire on
        :param missile_item_id: The optional ID of the missile to fire. If not set use the first available.
        """
        payload = optional({
            'targetId': target_id,
            'missileItemId': missile_item_id,
        }, ('missileItemId',))
        await self._add_task(mid, 'ignite_missile', payload)

    async def transfer_deuterium_from_external_storage(self, mid: str, object_id: str, amount: float):
        """Transfer raw deuterium from external storage into the probe tank

        Retrieves deuterium stored as raw material in accessible external storage in the current sector,
        and fills the selected probe's deuterium tank directly. Requires an idle embarked Manny and a stationary probe.
        amount is expressed in ECE: 0.01 ECE adds 1 tank point (100 points per ECE), regardless of tank model or compression.
        The task always takes 600 seconds: five minutes outbound and five minutes returning, in a single trip
        regardless of the quantity. The tank is credited only at completion.
        Requests exceeding the remaining unreserved tank capacity are accepted with 202 and reduced to that capacity,
        rounded down to 0.0001 ECE. transfer.tankTransfer reports requestedAmountEce, acceptedAmountEce,
        tankPoints and clamped. Only the accepted amount must be available at the source.
        A full or fully reserved tank returns 409 probe_deuterium_full; insufficient source stock returns 422.
        Raw stock and incoming tank capacity are reserved atomically. No onboard cargo capacity is required.
        Capacity is checked again on return: any amount that no longer fits is released back to source stock,
        without loss. The final result includes deliveredTankPoints and delivered, released and lost resources in ECE.
        Cancellation, probe departure or source relocation releases reservations. If the Manny is destroyed,
        only deuterium carried on the return leg is lost; the outbound leg carries no deuterium.
        Idempotency-Key is account-wide and binds method, path and canonical JSON. Matching retries return
        the original response even after completion. The transfer can be followed with
        GET /api/probe/{probeId}/storage-transfers/{transferId}.

        :param mid: The ID of the manny to carry out the task
        :param object_id: The ID of the external storage
        :param amount: The amount of deuterium to refuel
        """
        payload = {
            'objectId': object_id,
            'amount': amount,
        }
        await self._add_task(mid, 'transfer-deuterium-from-external-storage', payload)


class MannySub(APISub):

    async def get(self, pid: int, mid: str) -> APIResponse[Manny]:
        """Returns the selected Manny's last persisted state with the same visibility and task-detail rules as the Manny list endpoint.
        The read never completes a task; only the scheduler worker applies time-based Manny transitions.

        :param pid: ID of the probe the manny belongs to
        :param mid: ID of the manny to query for
        """
        return await self.client.api_call('get',
                                          f'probe/{pid}/mannies/{mid}',
                                          None,
                                          lambda inp: Manny.from_dict(inp['manny']))

    async def get_all(self, pid: int) -> APIResponse[Dict[str, Manny]]:
        """Returns all mannies for the given probe.

        :param pid: Probe ID"""
        data = await self.client.api_call('get',
                                          f'probe/{pid}/mannies',
                                          None,
                                          lambda inp: {x['id']: Manny.from_dict(x) for x in inp['mannies']})
        return data

    async def rename(self, pid: int, mid: str, new_name: str) -> APIResponse[Manny]:
        """Renames a mannie.

        :param pid: Probe ID
        :param mid: Manny ID
        :param new_name: The new name of the mannie
        :return The newly updated manny
        """
        data = await self.client.api_call('patch',
                                          f'probe/{pid}/mannies/{mid}',
                                          {'name': new_name},
                                          lambda inp: Manny.from_dict(inp['manny']))
        if data.success:
            await self.client.issue_cache_update(data.data)
        return data

    async def repair(self, pid: int, mid: str, percent: int) -> APIResponse[Manny]:
        """Repair a probe with a mannie."""
        data = await self.client.api_call('post',
                                          f'probe/{pid}/mannies/{mid}/repair',
                                          {'integrityPercent': percent},
                                          lambda inp: Manny.from_dict(inp['manny']))
        if data.success:
            await self.client.issue_cache_update(data.data)
        return data

    async def start_atomic_print(self, pid: int, recipe: Printable, mid: str | None = None) -> APIResponse[PrintResponse]:
        """Starts a recipe whose `craftableBy` includes `atomic_3d_printer`. The atomic printer reserves one available Manny aboard the probe for
        loading and unloading; that Manny exposes the `assisting_atomic_printer` task until the craft completes or is recalled.

        :param pid: Probe ID
        :param recipe: The recipe to craft
        :param mid: Optional ID of manny to craft with, if None use first free
        """
        data = await self.client.api_call('post',
                                          f'probe/{pid}/atomic-printer/craft',
                                          remove_none({'recipe': recipe, 'mannyId': mid}),
                                          lambda inp: PrintResponse.from_dict(inp))
        if data.success:
            await self.client.issue_cache_update(data.data.manny)
            await self.client.issue_cache_update(data.data.inventory)
        return data

    async def ignite_missile(self, pid: int, mid: str, target_id: str, missile_item_id: str | None = None) -> APIResponse[None]:
        """Starts a one-minute missile preparation with the selected embarked Manny.
        When missileItemId is omitted, the first available missile in the probe inventory is used.

        :param pid: Probe ID
        :param mid: The ID of the manny to carry out the task
        :param target_id: The ID of the target to fire on
        :param missile_item_id: The optional ID of the missile to fire. If not set use the first available.
        """
        payload = optional({
            'targetId': target_id,
            'missileItemId': missile_item_id,
        }, ('missileItemId',))
        return await self.client.api_call('post', f'probe/{pid}/mannies/{mid}/ignite_missile', payload, None)

    def tasks(self, pid: int):
        return MannyTaskManager(self.client, pid)
