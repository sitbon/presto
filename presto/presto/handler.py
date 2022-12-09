from __future__ import annotations

from typing import Type, TypeVar, Self, Optional

from copy import deepcopy
import requests

from presto.adict import adict
from .request import Request
from .response import Response

__all__ = "Handler",

PrestoT = TypeVar("PrestoT", bound="Presto")


# noinspection PyPep8Naming
class Handler:
    """Base request handler."""

    _presto: PrestoT

    _session: Optional[requests.Session] = None

    def __init__(
            self,
            presto: PrestoT,
    ):
        self._presto = presto

    def __call__(self, request: Request, **kwds) -> Response:
        request = deepcopy(request)
        if not isinstance(request, self._presto.Request) and not isinstance(request, type(self._presto)):
            raise TypeError(f"request must be of type {self._presto.Request.__name__} or {self._presto.__name__}")
        req = adict(request.__request__)
        req.__merge__(kwds)
        req.url = request.__url__

        return self._presto.Response(self, request, self.session.request(**req))

    @property
    def APPEND_SLASH(self) -> bool:
        return self._presto.APPEND_SLASH

    @property
    def presto(self) -> PrestoT:
        return self._presto

    @property
    def session(self) -> requests.Session:
        if self._session is None:
            self._session = requests.Session()
        return self._session

    def __copy__(self) -> Self:
        this = self.__class__.__new__(self.__class__)
        this._presto = self._presto
        this._session = self._session
        return this

    def __deepcopy__(self, memo: dict) -> Self:
        this = self.__class__.__new__(self.__class__)
        this._presto = self._presto
        return this
