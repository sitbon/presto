from typing import TypeVar

import httpx

from presto.presto import Presto

__all__ = "AsyncResponse",

HandlerT = TypeVar("HandlerT", bound="AsyncHandler")
RequestT = TypeVar("RequestT", bound="AsyncRequest")


class AsyncResponse(httpx.Response, Presto.Response):
    # noinspection PyMissingConstructor
    def __init__(self, handler: HandlerT, request: RequestT, response: httpx.Response):
        Presto.Response.__init__(self, handler, request, response)
