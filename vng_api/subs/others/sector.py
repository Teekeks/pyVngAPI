from vng_api.base import APISub, APIResponse
from vng_api.helper.internal import build_url
from vng_api.types import Vector
from vng_api.types.others import OthersSectorObservation


class OthersSectorSub(APISub):

    async def get(self, sid: str, location: Vector = None, x: int = None, y: int = None, z: int = None) -> APIResponse[OthersSectorObservation]:
        """Observe a sector using one owned Others fleet

        The coordinates are relative to the owning player's home; absolute coordinates are never exposed. shipId designates the owned fleet, and
        the closest active fleet ship supplies the scan. Precision follows the same distance, residence-time and visited-sector rules as GET
        /api/sector, using only this fleet's private visit history. A detailed observation includes detected probes and ships, with their current
        statuses, only when at least one active ship of the designated fleet is physically present in the requested sector. In that local case, every
        planet representation also exposes harvestable, which is true only while its remaining resources total more than 5 ECE. The probes
        property, detected ship objects and harvestable fields are otherwise omitted, including from precise historical observations.

        :param sid: Ship ID
        :param location: using Vector as origin, if set, x, y and z are ignored
        :param x: x coordinate, ignored if location is set
        :param y: y coordinate, ignored if location is set
        :param z: z coordinate, ignored if location is set
        :raises ValueError: If location is not set and one of x, y and z is also not set
        """
        if location is not None:
            x, y, z = location
        if any([x is None, y is None, z is None]):
            raise ValueError('missing coordinates')
        url = build_url('others/sector', {'shipId': sid, 'x': x, 'y': y, 'z': z})
        return await self.client.api_call('get', url, None, lambda inp: OthersSectorObservation.from_dict(inp['sector']))
