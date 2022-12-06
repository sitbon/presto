from __future__ import annotations

from typing import Type, TypeVar

import requests

from .request import _Request
from .response import _Response
from .adict import adict

__all__ = "_Handler",

PrestoT = TypeVar("PrestoT", bound="Presto")


class _Handler:

    Request: Type[_Request]
    Response: Type[_Response]

    __presto: PrestoT
    __session: requests.Session

    # noinspection PyPep8Naming,PyShadowingNames
    def __init__(
            self,
            presto: PrestoT,
            Request: Type[_Request],
            Response: Type[_Response]
    ):
        self.__presto = presto
        self.__session = requests.Session()
        self.Request = Request
        self.Response = Response

    def __call__(self, request: _Request, **kwds) -> _Response:
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
