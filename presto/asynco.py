from typing import Optional, TypeAlias, TypeVar, Self, Type

import httpx

from presto.presto import Presto

__all__ = "AsyncPresto",

AsyncPrestoT: TypeAlias = TypeVar("AsyncPrestoT", bound="AsyncPresto")
HandlerT: TypeAlias = TypeVar("HandlerT", bound="AsyncPresto.Request.Handler")


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

    def __call__(self, url: Optional[str] = None, **kwds) -> Self:
        if url is None and not kwds:
            raise RuntimeError("Use async method by awaiting .A directly.")

        return super().__call__(url=url, **kwds)

    class Client(Presto.Client):
        def __init__(self, presto: AsyncPrestoT):
            super().__init__(presto)
