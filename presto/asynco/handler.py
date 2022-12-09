from typing import TypeVar, Self, Optional, Type

from copy import deepcopy
import httpx

from presto.adict import adict
from presto.presto import Presto

from .request import AsyncRequest
from .response import AsyncResponse

__all__ = "AsyncHandler",


PrestoT = TypeVar("PrestoT", bound="AsyncPresto")


class AsyncHandler(Presto.Handler):

    _client: Optional[httpx.AsyncClient] = None

    async def __call__(self, request: AsyncRequest, **kwds) -> AsyncResponse:
        request = deepcopy(request)
        url = request.__url__
        params = adict(request.__request__).__merge__(kwds)
        method = params.pop("method")
        return self._presto.Response(self, request, await self.client.request(method, url, **params))

    @property
    def client(self) -> httpx.AsyncClient:
        if self._client is None:
            self._client = httpx.AsyncClient()
        return self._client

    @property
    def session(self):
        return NotImplemented

    def __copy__(self) -> Self:
        this = super().__copy__()
        this._client = self._client
        return this

    def __deepcopy__(self, memo) -> Self:
        this = super().__deepcopy__(memo)
        this._client = self._client
        return this
