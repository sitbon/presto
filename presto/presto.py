from typing import Optional, Self, Type, TypeAlias

from copy import copy, deepcopy

from presto.adict import adict
from presto.request import Request
from presto.handler import Handler

__all__ = "Presto",

ClientT: TypeAlias = "Client"


# noinspection PyPep8Naming
class Presto(Request):

    Client: Type[ClientT]

    class Request(Request):
        class Handler(Handler):
            class Response(Handler.Response):
                ...

    __params__: adict = adict(
        method="GET",
        headers=dict(
            Accept="application/json",
        ),
    )

    def __init__(
            self,
            *,
            url: str,
            RequestType: Optional[Type[Request]] = None,
            APPEND_SLASH: Optional[bool] = None,
            **kwds
    ):
        self.Request = RequestType or self.Request

        super().__init__(
            parent=None,
            path=url,
            APPEND_SLASH=APPEND_SLASH,
            **kwds
        )

    def __copy__(self) -> Self:
        this: Self = super().__copy__()
        this.Request = self.Request
        return this

    @property
    def request(self) -> Request:
        return super().__getattr__("")

    def __call__(self, url: Optional[str] = None, **kwds) -> Self | Request.Handler.Response:
        if url is not None:
            if not kwds:
                this = copy(self)
                this.__path__ = url
                return this

            this = deepcopy(self)
            this.__path__ = url
            this.__merge__(**kwds)
            return this

        return super().__call__(**kwds)

    get = property(lambda self: self.request(method="GET"))
    post = property(lambda self: self.request(method="POST"))
    put = property(lambda self: self.request(method="PUT"))
    patch = property(lambda self: self.request(method="PATCH"))
    delete = property(lambda self: self.request(method="DELETE"))
    options = property(lambda self: self.request(method="OPTIONS"))
    head = property(lambda self: self.request(method="HEAD"))


class Client:
    """Very simple base class for Presto client API implementations."""

    P: Presto

    class Request(Presto.Request):
        class Handler(Presto.Request.Handler):
            class Response(Presto.Request.Handler.Response):
                RAISE_EXCEPT_FOR = {404}

    # noinspection PyPep8Naming
    def __init__(
            self,
            *,
            url: str,
            PrestoType: Optional[Type[Presto]] = None,
            RequestType: Optional[Type[Request]] = None,
            APPEND_SLASH: Optional[bool] = None,
            **kwds
    ):
        self.P = (PrestoType or Presto)(
            url=url,
            RequestType=RequestType or self.Request,
            APPEND_SLASH=APPEND_SLASH,
            **kwds,
        )

    @property
    def url(self):
        return self.P.__url__


Presto.Client = Client
