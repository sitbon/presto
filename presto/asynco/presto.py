from __future__ import annotations

from typing import Optional, Union, Type

import warnings

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

    A: AsyncResponse = presto.Presto.Request.__async__

    def __call__(self, url: Optional[str] = None, **kwds) -> Union[AsyncPresto, AsyncPresto.Response]:
        if not kwds:
            raise RuntimeError("Use async method by awaiting .A directly.")
        return super().__call__(url=url, **kwds)



