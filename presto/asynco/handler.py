from typing import Self, Optional

from copy import deepcopy
import httpx

from presto.adict import adict

from . import request, response

__all__ = "AsyncHandler",


class AsyncHandler(request.AsyncRequest.__Handler__):

    _client: Optional[httpx.AsyncClient] = None

    async def __call__(self, requ: request.AsyncRequest, **kwds) -> response.AsyncResponse:
        requ = deepcopy(requ)
        url = requ.__url__
        params = adict(requ.__merged__).__merge__(kwds)
        method = params.pop("method")
        return self._presto.Response(self, requ, await self.client.request(method, url, **params))

    @property
    def client(self) -> httpx.AsyncClient:
        if self._client is None:
            self._client = httpx.AsyncClient()
        return self._client

    def __copy__(self) -> Self:
        this: Self = super().__copy__()
        this._client = self._client
        return this

    def __deepcopy__(self, memo) -> Self:
        this: Self = super().__deepcopy__(memo)
        this._client = self._client
        return this
