from __future__ import annotations

from typing import Optional, Union, Self, Type

from copy import copy

from presto.presto import Presto

from .handler import AsyncHandler as _AsyncHandler
from .request import AsyncRequest as _AsyncRequest
from .response import AsyncResponse as _AsyncResponse

__all__ = "AsyncPresto",


# noinspection PyPep8Naming
class AsyncPresto(Presto):

    class AsyncHandler(_AsyncHandler):
        pass

    class AsyncRequest(_AsyncRequest):
        pass

    class AsyncResponse(_AsyncResponse):
        pass

    def __init__(
            self,
            url: str,
            *,
            Handler: Type[AsyncHandler[Presto]] = AsyncHandler,
            Request: Type[AsyncRequest[AsyncHandler[Presto]]] = AsyncRequest,
            Response: Type[AsyncResponse] = AsyncResponse,
            **kwds
    ):
        super().__init__(
            url=url,
            Handler=Handler,
            Request=Request,
            Response=Response,
            **kwds
        )

    async def __call__(self, url: Optional[str] = None, **kwds) -> Union[AsyncPresto, Self, AsyncResponse]:
        if url is not None:
            presto = copy(self)
            presto.__url__ = url + ("/" if self.APPEND_SLASH and url[-1:] != "/" else "")
            if kwds:
                return await presto.__call__(**kwds)
            return presto

        return await super().__call__(**kwds)
