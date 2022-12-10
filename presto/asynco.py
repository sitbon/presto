from typing import Optional, TypeAlias, TypeVar, Self, Type

import httpx

from presto.presto import Presto

__all__ = "AsyncPresto",

AsyncPrestoT: TypeAlias = TypeVar("AsyncPrestoT", bound="AsyncPresto")
HandlerT: TypeAlias = TypeVar("HandlerT", bound="AsyncPresto.Request.Handler")


# noinspection PyPep8Naming
class AsyncPresto(Presto):

    class Request(Presto.Request):
        class Handler(Presto.Request.Handler):

            _client: Optional[httpx.AsyncClient] = None

            class Response(httpx.Response, Presto.Request.Handler.Response):
                def __init__(self, hand: HandlerT, requ: Presto.Request, resp: httpx.Response):
                    Presto.Request.Handler.Response.__init__(self, hand, requ, resp)

            @property
            def client(self):
                if self._client is None:
                    self._client = httpx.AsyncClient()
                return self._client

            async def A(self, requ: Presto.Request) -> Response:
                method, url, params = self.__request__(requ)
                return self.Response(self, requ, await self.client.request(method, url, **params))

        def __call__(self, **kwds) -> Self:
            if not kwds:
                raise RuntimeError("Use async method by awaiting .A directly.")

            return super().__call__(**kwds)

    class Client(Presto.Client):
        # noinspection PyPep8Naming
        def __init__(
                self,
                url: str,
                *,
                PrestoType: Optional[Type[AsyncPrestoT]] = None,
                **kwds
        ):
            super().__init__(
                url=url,
                PrestoType=PrestoType or AsyncPresto,
                **kwds
            )
