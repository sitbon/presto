from __future__ import annotations

from typing import Optional, Union, Self, Type

from copy import copy

from presto import presto

from . import handler, request, response

__all__ = "AsyncPresto",


# noinspection PyPep8Naming
class AsyncPresto(presto.Presto):

    class AsyncHandler(handler.AsyncHandler):
        pass

    class AsyncRequest(request.AsyncRequest):
        pass

    class AsyncResponse(response.AsyncResponse):
        pass

    # noinspection PyPep8Naming
    def __init__(
            self,
            url: str,
            *,
            Handler: Optional[Type[AsyncPresto.AsyncHandler]] = None,
            Request: Optional[Type[AsyncPresto.AsyncRequest]] = None,
            Response: Optional[Type[AsyncPresto.AsyncResponse]] = None,
            **kwds
    ):
        super().__init__(
            url=url,
            Handler=Handler or self.AsyncHandler,
            Request=Request or self.AsyncRequest,
            Response=Response or self.AsyncResponse,
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
