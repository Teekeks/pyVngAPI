__all__ = []

from vng_api.types import Vector


def distance(v1: Vector, v2: Vector) -> int:
    """Returns the distance between vectors as seen by the games jump distance calculation.

    :param v1: First vector
    :param v2: Second vector
    :return: distance between v1 and v2
    """
    return max(abs(v1.x - v2.x), abs(v1.y - v2.y), abs(v1.z - v2.z))


def absolute_distance(v1: Vector, v2: Vector) -> int:
    """Returns the culmulative distance between the two given vectors along all axis.

    :param v1: First vector
    :param v2: Second vector
    :return: absolute distance between v1 and v2
    """
    return sum([abs(v1.x - v2.x), abs(v1.y - v2.y), abs(v1.z - v2.z)])
