__all__ = ['APIResponse', 'APIBatchResult', 'APIStats', 'APISub', 'BASEURL', 'ClientException', 'APICall', 'APIException']

from dataclasses import dataclass, field
from typing import List, TYPE_CHECKING

from aiohttp import ClientResponse

if TYPE_CHECKING:
    from vng_api.client import APIClient


BASEURL = 'https://neumann-probe.net/api/'


class ClientException(Exception):
    pass


class APIException(Exception):
    pass


@dataclass(frozen=True)
class APICall:
    method: str
    url: str
    data: dict | None


@dataclass
class APIResponse[T]:
    success: bool
    status: int
    error_message: str | None
    error_code: str | None
    data: T
    call: APICall

    def __iter__(self):
        return iter([self, self.data])

    def may_rise(self):
        """Will raise an exception if this API call failed"""
        if not self.success:
            msg = f'API call `{self.call.method} {self.call.url}` failed with status {self.status}'
            if self.error_code is not None:
                msg += f' | {self.error_code}: {self.error_message}'
            raise APIException(msg)


@dataclass
class APIBatchResult[T]:
    responses: List[APIResponse[T]] = field(default_factory=list)

    @property
    def success(self):
        return all(r.success for r in self.responses) if len(self.responses) > 0 else True


@dataclass
class APIStats:
    bucket_size: int = 0
    bucket_remaining: int = 0
    is_ratelimited: bool = False
    retry_after: int | None = None

    @property
    def bucket_used(self) -> int:
        return self.bucket_size - self.bucket_remaining

    def update_from_response(self, ret: ClientResponse):
        self.bucket_size = int(ret.headers.get('x-ratelimit-limit', 0))
        self.bucket_remaining = int(ret.headers.get('x-ratelimit-remaining', 0))
        self.is_ratelimited = ret.status == 429
        self.retry_after = int(ret.headers.get('retry-after'))


class APISub:

    client: "APIClient"

    def __init__(self, client: "APIClient"):
        self.client = client

