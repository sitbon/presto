from typing import TypeVar

import httpx

from presto import presto

__all__ = "AsyncResponse",

HandlerT = TypeVar("HandlerT", bound="AsyncHandler")
RequestT = TypeVar("RequestT", bound="AsyncRequest")


class AsyncResponse(httpx.Response, presto.Presto.Response):
    # noinspection PyMissingConstructor
    def __init__(self, handler: HandlerT, request: RequestT, response: httpx.Response):
        presto.Presto.Response.__init__(self, handler, request, response)
