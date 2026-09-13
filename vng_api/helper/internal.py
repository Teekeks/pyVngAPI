"""
A number of usefull helpers only designed to be used within the library itself.
"""
__all__ = ['remove_none', 'optional', 'build_url']

from urllib import parse
from enum import Enum
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


def build_url(url: str, params: dict) -> str:
    """Build a valid url string

    :param url: base URL
    :param params: dictionary of URL parameter
    :return: URL
    """

    def get_val(val):
        if isinstance(val, Enum):
            return str(val.value)
        return str(val)

    def add_param(res, k, v):
        if len(res) > 0:
            res += "&"
        res += str(k)
        if v is not None:
            res += "=" + parse.quote(get_val(v))
        return res

    result = ""
    for key, value in params.items():
        if value is None:
            continue
        if isinstance(value, list):
            for va in value:
                result = add_param(result, key, va)
        else:
            result = add_param(result, key, value)
    return url + (("?" + result) if len(result) > 0 else "")
