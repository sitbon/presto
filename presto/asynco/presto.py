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

    # noinspection PyPep8Naming
    def __init__(
            self,
            url: str,
            *,
            Handler: Optional[Type[AsyncPresto.Handler]] = None,
            Request: Optional[Type[AsyncPresto.Request]] = None,
            Response: Optional[Type[AsyncPresto.Response]] = None,
            **kwds
    ):
        super().__init__(
            url=url,
            Handler=Handler or self.Handler,
            Request=Request or self.Request,
            Response=Response or self.Response,
            **kwds
        )

    async def __call__(self, url: Optional[str] = None, **kwds) -> Union[AsyncPresto, Self, AsyncPresto.Response]:
        if url is not None:
            presto_ = copy(self)
            presto_.__url__ = url + ("/" if self.APPEND_SLASH and url[-1:] != "/" else "")
            if kwds:
                return await presto_.__call__(**kwds)
            return presto_

        return await super().__call__(**kwds)
