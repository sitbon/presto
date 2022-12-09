from __future__ import annotations

from typing import Optional, Union, Self, Type

from copy import copy

from presto import presto

from . import handler, request, response

__all__ = "AsyncPresto",


# noinspection PyPep8Naming
class AsyncPresto(presto.Presto):

    class Handler(handler.AsyncHandler):
        pass

    class Request(request.AsyncRequest):
        pass

    class Response(response.AsyncResponse):
        pass

    def __init__(
            self,
            url: str,
            *,
            Handler: Type[AsyncPresto.Handler] = Handler,
            Request: Type[AsyncPresto.Request] = Request,
            Response: Type[AsyncPresto.Response] = Response,
            **kwds
    ):
        super().__init__(
            url=url,
            Handler=Handler,
            Request=Request,
            Response=Response,
            **kwds
        )

    async def __call__(self, url: Optional[str] = None, **kwds) -> Union[AsyncPresto, Self, AsyncPresto.Response]:
        if url is not None:
            presto = copy(self)
            presto.__url__ = url + ("/" if self.APPEND_SLASH and url[-1:] != "/" else "")
            if kwds:
                return await presto.__call__(**kwds)
            return presto

        return await super().__call__(**kwds)
