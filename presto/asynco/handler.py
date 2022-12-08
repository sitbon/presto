from typing import TypeVar, Self, Optional

from copy import deepcopy
import httpx

from presto.adict import adict
from presto.presto import Presto

from .response import AsyncResponse

__all__ = "AsyncHandler",


PrestoT = TypeVar("PrestoT", bound="AsyncPresto")


class AsyncHandler(Presto.Handler):
    _session: Optional
    _client: httpx.AsyncClient

    def __init__(
            self,
            presto: PrestoT,
    ):
        super().__init__(presto)
        self._session = None
        self._client = httpx.AsyncClient()

    async def __call__(self, request: Presto.Request, **kwds) -> Presto.Response:
        request = deepcopy(request)
        url = request.__url__
        params = adict(request.__request__).__merge__(kwds)
        method = params.pop("method")
        return self.presto.Response(self, request, await self._client.request(method, url, **params))

    @property
    def client(self):
        return self._client

    def __copy__(self) -> Self:
        this = super().__copy__()
        this._client = self._client
        return this

    def __deepcopy__(self, memo: dict) -> Self:
        this = super().__deepcopy__(memo)
        this._session = None
        this._client = httpx.AsyncClient()
        return this
