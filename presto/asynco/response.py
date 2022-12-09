import httpx

from presto import presto

from . import request

__all__ = "AsyncResponse",


class AsyncResponse(httpx.Response, request.AsyncRequest.__Response__):
    def __init__(self, hand: request.HandlerT, requ: request.AsyncRequest, resp: httpx.Response):
        presto.Presto.Response.__init__(self, hand, requ, resp)
