"""
A number of usefull helpers only designed to be used within the library itself.
"""
__all__ = ['remove_none', 'optional']

from typing import Dict, Any, Iterable


def remove_none(inp: Dict[Any, Any]) -> Dict[Any, Any]:
    """removes keys with None values from the given dictionary

    :param inp: dictionary to remove keys from"""
    return {k: v for k, v in inp.items() if v is not None}


def optional[T](inp: Dict[T, Any], opt_keys: Iterable[T]) -> Dict[T, Any]:
    """removes entries from the given dictionary that are None and in the opt_keys list

    :param inp: input dictionary
    :param opt_keys: list of keys to check for removal
    """
    return {k: v for k, v in inp.items() if (True if k not in opt_keys else v is not None)}
