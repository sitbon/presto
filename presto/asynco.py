from typing import Optional, TypeAlias, Self, Type

import httpx

from presto.presto import Presto

__all__ = "AsyncPresto",

HandlerT: TypeAlias = "AsyncPresto.Request.Handler"
ClientT: TypeAlias = "Client"


class AsyncPresto(Presto):

    Client: Type[ClientT]

    class Request(Presto.Request):
        class Handler(Presto.Request.Handler):

            _client: Optional[httpx.AsyncClient] = None

            class Response(httpx.Response, Presto.Request.Handler.Response):
                def __init__(self, hand: HandlerT, requ: Presto.Request, resp: httpx.Response):
                    Presto.Request.Handler.Response.__init__(self, hand, requ, resp)

            @property
            def client(self) -> httpx.AsyncClient:
                if self._client is None:
                    self._client = httpx.AsyncClient()
                return self._client

            async def A(self, requ: Presto.Request) -> Response:
                method, url, params = self.__request__(requ)
                return self.Response(self, requ, await self.client.request(method, url, **params))

        def __call__(self, **kwds) -> Self:
            if not kwds:
                return self.A

            return super().__call__(**kwds)

    def __call__(self, url: Optional[str] = None, **kwds) -> Self:
        if url is None and not kwds:
            return self.A

        return super().__call__(url=url, **kwds)


# noinspection PyPep8Naming
class Client(Presto.Client):
    def __init__(
            self,
            *,
            url: str,
            PrestoType: Optional[Type[AsyncPresto]] = None,
            RequestType: Optional[Type[AsyncPresto.Request]] = None,
            APPEND_SLASH: Optional[bool] = None,
            **kwds
    ):
        super().__init__(
            url=url,
            PrestoType=PrestoType or AsyncPresto,
            RequestType=RequestType or self.Request,
            APPEND_SLASH=APPEND_SLASH,
            **kwds
        )


AsyncPresto.Client = Client
