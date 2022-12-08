import httpx

from presto.presto import Presto

__all__ = "Response",


class Response(httpx.Response, Presto.Response):
    # noinspection PyMissingConstructor
    def __init__(self, response: httpx.Response):
        Presto.Response.__init__(self, response)
