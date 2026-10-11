__all__ = ['distance', 'absolute_distance', 'neighbours']

from typing import List

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


_NEIGHBOUR_OFFSETS = [
        [1, 1, 0],
        [1, -1, 0],
        [-1, 1, 0],
        [-1, -1, 0],
        [1, 0, 1],
        [1, 0, -1],
        [-1, 0, 1],
        [-1, 0, -1],
        [0, 1, 1],
        [0, 1, -1],
        [0, -1, 1],
        [0, -1, -1],
    ]


def neighbours(v: Vector) -> List[Vector]:
    """Returns a list of neighbouring vectors.
    :param v: Origin vector
    """
    return [Vector.from_dict({'x': i[0] + v.x, 'y': i[1] + v.y, 'z': i[2] + v.z}) for i in _NEIGHBOUR_OFFSETS]
