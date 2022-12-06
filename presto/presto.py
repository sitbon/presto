from __future__ import annotations

from typing import Optional, Union, Type, Self

from .handler import _Handler
# noinspection PyProtectedMember
from .request import AbstractRequest, _Request
from .response import _Response
from .adict import adict

__all__ = "Presto",


class Presto(AbstractRequest):

    Handler: Type[_Handler] = _Handler
    Request: Type[_Request] = _Request
    Response: Type[_Response] = _Response

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
            Handler: Type[_Handler] = Handler,
            Request: Type[_Request] = Request,
            Response: Type[_Response] = Response,
            APPEND_SLASH: bool = APPEND_SLASH,
            **kwds
    ):
        self.Handler = Handler
        self.Request = Request
        self.Response = Response
        self.APPEND_SLASH = APPEND_SLASH
        self.__handler__ = Handler(
            presto=self, Request=Request, Response=Response
        )
        self.__url__ = url + ("/" if self.APPEND_SLASH and url[-1:] != "/" else "")
        super().__init__(self, **kwds)

    def __repr__(self):
        return f"{self.__class__.__name__}(url={self.__url__!r}, params={self.__params__!r})"

    def __call__(self, url: Optional[str] = None, **kwds) -> Union[Presto, Self, Response]:
        if url is not None:
            presto = self.copy()
            presto.__url__ = url + ("/" if self.APPEND_SLASH and url[-1:] != "/" else "")
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

    def copy(self) -> Self:
        this = super().copy()
        this.Handler = self.Handler
        this.Request = self.Request
        this.Response = self.Response
        this.APPEND_SLASH = self.APPEND_SLASH
        this.__url__ = self.__url__
        return this
