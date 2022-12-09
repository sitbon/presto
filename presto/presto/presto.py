from typing import Optional, Union, Type, Self, TypeAlias, TypeVar

from copy import copy, deepcopy

from . import handler, request, response

__all__ = "Presto",

HandlerT: TypeAlias = TypeVar("HandlerT", bound="Presto.Handler")
RequestT: TypeAlias = TypeVar("RequestT", bound="Presto.Request")
ResponseT: TypeAlias = TypeVar("ResponseT", bound="Presto.Response")


class Presto(request.Request.__Request__):

    APPEND_SLASH: bool = False

    __url: str = ""

    class Handler(handler.Handler):
        """"""

    class Request(request.Request):
        """"""

    class Response(response.Response):
        """"""

    __params__: dict = dict(
        method="GET",
        headers=dict(
            Accept="application/json",
        ),
    )

    # noinspection PyPep8Naming
    def __init__(
            self,
            url: str,
            *,
            Handler: Optional[Type[HandlerT]] = None,
            Request: Optional[Type[RequestT]] = None,
            Response: Optional[Type[ResponseT]] = None,
            APPEND_SLASH: Optional[bool] = None,
            **kwds
    ):
        self.APPEND_SLASH = APPEND_SLASH if APPEND_SLASH is not None else self.APPEND_SLASH
        super().__init__(None, **kwds)
        self.__url__ = url
        self.Handler = Handler or self.Handler
        self.Request = Request or self.Request
        self.Response = Response or self.Response
        self.__handler__ = self.Handler(presto=self)

    @property
    def __url__(self) -> str:
        return self.__url

    @__url__.setter
    def __url__(self, url: str):
        self.__url = url + ("/" if self.APPEND_SLASH and url[-1:] != "/" else "")

    @property
    def request(self) -> Request:
        req = self.Request(self, "")
        req.__requests__.update(self.__requests__)
        return req

    def __call__(self, url: Optional[str] = None, **kwds) -> Union[Self, Response]:
        if url is not None:
            presto = copy(self)
            presto.__url__ = url
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
        this: Self = super().__copy__()
        this.__handler__._presto = this
        this.APPEND_SLASH = self.APPEND_SLASH
        this.__url__ = self.__url__
        this.Handler = self.Handler
        this.Request = self.Request
        this.Response = self.Response
        return this

    def __deepcopy__(self, memo: dict) -> Self:
        this: Self = super().__deepcopy__(memo)
        this.__handler__._presto = this
        this.APPEND_SLASH = self.APPEND_SLASH
        this.__url__ = self.__url__
        this.Handler = deepcopy(self.Handler, memo)
        this.Request = deepcopy(self.Request, memo)
        this.Response = deepcopy(self.Response, memo)
        return this
