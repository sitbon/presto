from __future__ import annotations

from typing import Optional, Union, Type, Self

from copy import copy, deepcopy

from presto.adict import adict
from . import handler, request, response

__all__ = "Presto",


class Presto(request.__Request__):

    APPEND_SLASH: bool = False

    __url__: str = None

    class Handler(handler.Handler):
        """"""

    class Request(request.Request):
        """"""

    class Response(response.Response):
        """"""

    __params__: adict = adict(
        method="GET",
        headers=adict(
            Accept="application/json",
        ),
    )

    # noinspection PyPep8Naming
    def __init__(
            self,
            url: str,
            *,
            Handler: Optional[Type[Presto.Handler]] = None,
            Request: Optional[Type[Presto.Request]] = None,
            Response: Optional[Type[Presto.Response]] = None,
            APPEND_SLASH: Optional[bool] = None,
            **kwds
    ):
        self.APPEND_SLASH = APPEND_SLASH if APPEND_SLASH is not None else self.APPEND_SLASH
        super().__init__(self, **kwds)
        self.__url__ = url + ("/" if self.APPEND_SLASH and url[-1:] != "/" else "")
        self.Handler = Handler or self.Handler
        self.Request = Request or self.Request
        self.Response = Response or self.Response
        self.__handler__ = self.Handler(presto=self)

    @property
    def request(self) -> Presto.Request:
        req = self.Request(self, "")
        req.__requests__.update(self.__requests__)
        return req

    def __call__(self, url: Optional[str] = None, **kwds) -> Union[Presto, Self, Presto.Response]:
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
        this.__handler__._presto = this
        this.APPEND_SLASH = self.APPEND_SLASH
        this.__url__ = self.__url__
        this.Handler = deepcopy(self.Handler, memo)
        this.Request = deepcopy(self.Request, memo)
        this.Response = deepcopy(self.Response, memo)
        return this
