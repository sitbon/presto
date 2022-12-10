from typing import Optional, TypeAlias, TypeVar, Any, Self

import requests

from presto.adict import adict
from presto.request import Request

__all__ = "Handler",

HandlerT: TypeAlias = TypeVar("HandlerT", bound="Handler")


class Handler(Request.Handler):
    """Base request handler."""

    __session: Optional[requests.Session] = None

    class Response(requests.Response, Request.Handler.Response):
        __attr: Optional[adict] = None

        def __init__(self, hand: HandlerT, requ: Request, resp: requests.Response):
            self.__dict__ = resp.__dict__
            self.__attr = None
            Request.Handler.Response.__init__(self, hand, requ)

        @property
        def attr(self):
            if self.__attr is None:
                if self.status_code == 200 and \
                        self.headers.get("content-type").startswith("application/json"):
                    self.__attr = adict(self.json())
            return self.__attr

        def _raise_for_status(self):
            if self._should_raise_for_status(self.status_code):
                self.raise_for_status()

    async def A(self, requ: Request) -> Response:
        return self.__call__(requ)

    @classmethod
    def __request__(cls, requ: Request) -> tuple[str, str, dict[str, Any]]:
        url = requ.__url__
        rreq = requ.__merged__
        method = rreq.pop("method")
        return method, url, rreq

    def __call__(self, requ: Request) -> Response:
        method, url, rreq = self.__request__(requ)
        return self.Response(
            hand=self,
            requ=requ,
            resp=self.session.request(
                method=method,
                url=url,
                **rreq
            )
        )

    def call(self, requ: Request) -> Response:
        return Handler.__call__(self, requ)

    @property
    def session(self) -> requests.Session:
        if self.__session is None:
            self.__session = requests.Session()
        return self.__session

    def __copy__(self) -> Self:
        this: Self = self.__class__.__new__(self.__class__)
        this.__session = self.__session
        return this

    def __deepcopy__(self, memo: dict[int, Any]) -> Self:
        this = self.__copy__()
        this.__session = None
        return this
