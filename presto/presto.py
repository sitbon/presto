from typing import Optional, Type, Self, TypeAlias, TypeVar

from copy import deepcopy

from presto.adict import adict
from presto.request import Request
from presto.handler import Handler

__all__ = "Presto",

PrestoT: TypeAlias = TypeVar("PrestoT", bound="Presto")


# noinspection PyPep8Naming
class Presto(Request):

    class Request(Request):
        class Handler(Handler):
            class Response(Handler.Response):
                ...

    __params__: dict = dict(
        method="GET",
        headers=dict(
            Accept="application/json",
        ),
    )

    def __init__(
            self,
            url: str,
            *,
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
        """Base class for Presto client API implementations."""

        _presto: PrestoT

        _params: adict | dict = dict(
            method="GET",
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
            },
        )

        # noinspection PyPep8Naming
        def __init__(
                self,
                url: str,
                *,
                PrestoType: Optional[Type[PrestoT]] = None,
                **kwds
        ):
            params = adict.__merged__(self._params, kwds) if kwds else adict(self._params)

            presto_t = PrestoType or Presto

            self._presto = presto_t(
                url=url,
                RequestType=presto_t.Request,
                **params,
            )

        @property
        def url(self):
            return self._presto.__url__
