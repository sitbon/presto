from __future__ import annotations

from typing import Type, TypeVar, Generic

import requests

from .request import _Request
from .response import _Response
from .adict import adict

__all__ = "_Handler",

PrestoT = TypeVar("PrestoT", bound="Presto")


class _Handler(Generic[PrestoT]):
    """Base request handler.

    Contract in order to prevent circular structure:
        This class carries no state from the Presto instance passed to __init__.
        (That lambda doesn't count :)
    """

    APPEND_SLASH: bool

    _Presto: Type[PrestoT]

    Request: Type[_Request[_Handler[PrestoT]]]
    Response: Type[_Response]

    __session: requests.Session

    # noinspection PyPep8Naming,PyShadowingNames
    def __init__(
            self,
            presto: PrestoT,
            Request: Type[_Request[_Handler[PrestoT]]] = _Request,
            Response: Type[_Response] = _Response,
    ):
        # noinspection PyTypeChecker
        self.APPEND_SLASH = property(lambda self: presto.APPEND_SLASH)
        self._Presto = type(presto)
        self.__session = requests.Session()
        self.Request = Request
        self.Response = Response

    def __call__(self, request: _Request[_Handler[PrestoT]], **kwds) -> _Response:
        if not isinstance(request, self.Request) and not isinstance(request, self._Presto):
            raise TypeError(f"request must be of type {self.Request.__name__} or {self._Presto.__name__}")

        req = adict(request.__request__)
        req.merge(kwds)
        req.url = request.__url__

        return self.Response(self.session.request(**req))

    @property
    def session(self):
        return self.__session
