from typing import TypeVar, Self, Optional

from copy import deepcopy
import httpx

from presto.adict import adict
from presto.presto import Presto

from .response import Response

__all__ = "Handler",


PrestoT = TypeVar("PrestoT", bound="Presto")


class Handler(Presto.Handler):
    _client: httpx.AsyncClient

    def __init__(
            self,
            presto: PrestoT,
    ):
        self._presto = presto
        self._client = httpx.AsyncClient()

    async def __call__(self, request: Presto.Request, **kwds) -> Presto.Response:
        url = request.__url__
        params = adict(request.__request__).__merge__(kwds)
        method = params.pop("method")
        return Response(await self._client.request(method, url, **params))

    @property
    def client(self):
        return self._client

    def __copy__(self) -> Self:
        this = self.__class__.__new__(self.__class__)
        this._presto = self._presto
        this._client = self._client
        return this

    def __deepcopy__(self, memo: dict, to: Optional[PrestoT] = None) -> Self:
        if id(self) in memo:
            return memo[id(self)]  # For when Presto calls this directly.
        this = self.__class__.__new__(self.__class__)
        memo[id(self)] = this
        this._presto = to or deepcopy(self._presto, memo)
        this._client = httpx.AsyncClient()
        return this
