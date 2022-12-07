from __future__ import annotations

from typing import Type, TypeVar, Generic, Self, Optional

from copy import deepcopy
import requests

from .request import _Request
from .response import _Response
from .adict import adict

__all__ = "_Handler",

PrestoT = TypeVar("PrestoT", bound="Presto")


# noinspection PyPep8Naming
class _Handler(Generic[PrestoT]):
    """Base request handler."""

    APPEND_SLASH: bool

    _presto: PrestoT

    Request: Type[_Request[_Handler[PrestoT]]]
    Response: Type[_Response]

    _session: requests.Session

    def __init__(
            self,
            presto: PrestoT,
    ):
        self._presto = presto
        self._session = requests.Session()

    def __call__(self, request: _Request[_Handler[PrestoT]], **kwds) -> _Response:
        if not isinstance(request, self.Request) and not isinstance(request, type(self._presto)):
            raise TypeError(f"request must be of type {self.Request.__name__} or {self._presto.__name__}")

        req = adict(request.__request__)
        req.merge(kwds)
        req.url = request.__url__

        return self.Response(self.session.request(**req))

    @property
    def APPEND_SLASH(self):
        return self._presto.APPEND_SLASH

    @property
    def Request(self) -> Type[_Request[_Handler[PrestoT]]]:
        return self._presto.Request

    @property
    def Response(self) -> Type[_Response]:
        return self._presto.Response

    @property
    def session(self):
        return self._session

    def __copy__(self) -> Self:
        this = self.__class__.__new__(self.__class__)
        this._presto = self._presto
        this._session = self._session
        return this

    def __deepcopy__(self, memo: dict, to: Optional[PrestoT] = None) -> Self:
        if id(self) in memo:
            return memo[id(self)]  # For when Presto calls this directly.
        this = self.__class__.__new__(self.__class__)
        memo[id(self)] = this
        this._presto = to or deepcopy(self._presto, memo)
        this._session = requests.Session()
        return this
