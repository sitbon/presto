from typing import Optional, TypeAlias, Self

from copy import deepcopy
import requests

from presto.adict import adict

from . import request, response

__all__ = "Handler",

PrestoT: TypeAlias = request.RequestT


# noinspection PyPep8Naming
class Handler(request.Request.__Handler__):
    """Base request handler."""

    _presto: PrestoT

    _session: Optional[requests.Session] = None

    def __init__(
            self,
            presto: PrestoT,
    ):
        self._presto = presto

    def __call__(self, requ: request.Request, **kwds) -> response.Response:
        requ = deepcopy(requ)
        if not isinstance(requ, self._presto.Request) and not isinstance(requ, type(self._presto)):
            raise TypeError(f"request must be of type {self._presto.Request.__name__} or {self._presto.__name__}")
        resreq = adict(requ.__merged__)
        resreq.__merge__(kwds)
        resreq.url = requ.__url__

        return self._presto.Response(self, resreq, self.session.request(**resreq))

    def call(self, requ: request.Request) -> response.Response:
        return Handler.__call__(self, requ)

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
