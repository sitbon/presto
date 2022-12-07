from __future__ import annotations

from typing import Optional, Union, Type, Self

from copy import copy, deepcopy

from .handler import _Handler
# noinspection PyProtectedMember
from .request import __Request__, _Request
from .response import _Response
from .adict import adict

__all__ = "Presto",


# noinspection PyPep8Naming
class Presto(__Request__):

    APPEND_SLASH: bool = False

    __url__: str = None

    Handler: Type[_Handler[Presto]] = _Handler
    Request: Type[_Request[_Handler[Presto]]] = _Request
    Response: Type[_Response] = _Response

    __params__: adict = adict(
        method="GET",
        headers=adict(
            Accept="application/json",
        ),
    )

    def __init__(
            self,
            url: str,
            *,
            Handler: Type[_Handler[Presto]] = _Handler,
            Request: Type[_Request[_Handler[Presto]]] = _Request,
            Response: Type[_Response] = _Response,
            APPEND_SLASH: bool = APPEND_SLASH,
            **kwds
    ):
        self.APPEND_SLASH = APPEND_SLASH
        self.__url__ = url + ("/" if self.APPEND_SLASH and url[-1:] != "/" else "")
        self.Handler = Handler
        self.Request = Request
        self.Response = Response
        self.__handler__ = Handler(presto=self)
        super().__init__(self, **kwds)

    @property
    def request(self):
        request = self.__handler__.Request(self, "")
        request.__requests__.update(self.__requests__)
        return request

    def __call__(self, url: Optional[str] = None, **kwds) -> Union[Presto, Self, Response]:
        if url is not None:
            presto = copy(self)
            presto.__url__ = url + ("/" if self.APPEND_SLASH and url[-1:] != "/" else "")
            if kwds:
                return presto.__call__(**kwds)
            return presto

        return super().__call__(**kwds)

    get = property(lambda self: self.request(method="GET"))
    post = property(lambda self: self.request(method="POST"))
    put = property(lambda self: self.request(method="PUT"))
    patch = property(lambda self: self.request(method="PATCH"))
    delete = property(lambda self: self.request(method="DELETE"))
    options = property(lambda self: self.request(method="OPTIONS"))
    head = property(lambda self: self.request(method="HEAD"))

    def __copy__(self) -> Self:
        this = super().__copy__()
        this.__handler__._presto = this
        this.APPEND_SLASH = self.APPEND_SLASH
        this.__url__ = self.__url__
        this.Handler = self.Handler
        this.Request = self.Request
        this.Response = self.Response
        return this

    def __deepcopy__(self, memo: dict) -> Self:
        this = super().__deepcopy__(memo)
        this.__handler__ = self.__handler__.__deepcopy__(memo, this)
        this.APPEND_SLASH = self.APPEND_SLASH
        this.__url__ = self.__url__
        this.Handler = deepcopy(self.Handler, memo)
        this.Request = deepcopy(self.Request, memo)
        this.Response = deepcopy(self.Response, memo)
        return this
