from __future__ import annotations

from typing import Type, Any, TypeVar

import requests

from .typing import AttrCopyable
from .request import Request
from .response import Response
from .adict import adict

__all__ = "Handler",

TRequestType = TypeVar("TRequestType", bound=Type[Request])
TResponseType = TypeVar("TResponseType", bound=Type[Response])
TPresto = TypeVar("TPresto", bound="Presto")


class Handler(AttrCopyable):
    __state_attrs__ = "Request", "Response", "_Handler__presto"

    Request: Type[Request]
    Response: Type[Response]

    __presto: TPresto
    __session: requests.Session

    # noinspection PyPep8Naming,PyShadowingNames
    def __init__(
            self,
            presto: TPresto,
            Request: TRequestType,
            Response: TResponseType
    ):
        self.__presto = presto
        self.__session = requests.Session()
        self.Request = Request
        self.Response = Response

    def __set_state__(self, state, memo=None):
        super().__set_state__(state, memo)
        self.__session = requests.Session()

    def __call__(self, request: Request, **kwds) -> Response:
        if not isinstance(request, self.Request) and not isinstance(request, type(self.presto)):
            raise TypeError(f"request must be of type {self.Request.__name__} or {type(self.presto).__name__}")

        req = adict(request.__request__)
        req.merge(kwds)
        req.url = request.__url__

        return self.Response(self.session.request(**req))

    @property
    def presto(self):
        return self.__presto

    @property
    def session(self):
        return self.__session

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Handler):
            return False

        if other is self:
            return True

        return self.Request == other.Request and self.Response == other.Response
