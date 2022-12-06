from __future__ import annotations

from typing import Optional, Union, Type, Self

from .handler import Handler as PrestoHandler
# noinspection PyProtectedMember
from .request import AbstractRequest, Request as PrestoRequest
from .response import Response as PrestoResponse
from .adict import adict

__all__ = "Presto",


class Presto(AbstractRequest):
    __state_attrs__ = "APPEND_SLASH", "__url__",

    Handler: Type[PrestoHandler] = PrestoHandler
    Request: Type[PrestoRequest] = PrestoRequest
    Response: Type[PrestoResponse] = PrestoResponse

    APPEND_SLASH = False

    __url__: str = None

    __params__: adict = adict(
        method="GET",
        headers=adict(
            Accept="application/json",
        ),
    )

    # noinspection PyPep8Naming,PyShadowingNames
    def __init__(
            self,
            url: str,
            *,
            Handler: Type[PrestoHandler] = Handler,
            Request: Type[PrestoRequest] = Request,
            Response: Type[PrestoRequest] = Response,
            APPEND_SLASH: bool = APPEND_SLASH,
            **kwds
    ):
        self.APPEND_SLASH = APPEND_SLASH
        self.__handler__ = Handler(
            presto=self, Request=Request, Response=Response
        )
        self.__url__ = url + ("/" if self.APPEND_SLASH and url[-1:] != "/" else "")
        super().__init__(self, **kwds)

    def __repr__(self):
        return f"{self.__class__.__name__}(url={self.__url__!r}, params={self.__params__!r})"

    # # noinspection PyPep8Naming
    # @property
    # def Request(self) -> Type[Request]:
    #     return self.__handler__.Request
    #
    # # noinspection PyPep8Naming
    # @property
    # def Response(self) -> Type[Response]:
    #     return self.__handler__.Response

    def __call__(self, url: Optional[str] = None, **kwds) -> Union[Presto, Self, Response]:
        if url is not None:
            presto = self.__copy__()
            presto.__url__ = url
            return presto.__call__(**kwds)

        return super().__call__(**kwds)

    @property
    def request(self):
        request = self.__handler__.Request(self, "")
        request.__requests__.update(self.__requests__)
        return request

    get = property(lambda self: self.request(method="GET"))
    post = property(lambda self: self.request(method="POST"))
    put = property(lambda self: self.request(method="PUT"))
    patch = property(lambda self: self.request(method="PATCH"))
    delete = property(lambda self: self.request(method="DELETE"))
    options = property(lambda self: self.request(method="OPTIONS"))
    head = property(lambda self: self.request(method="HEAD"))
