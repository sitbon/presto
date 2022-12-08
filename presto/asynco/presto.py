from __future__ import annotations

from typing import Optional, Union, Self

from copy import copy

from presto import presto as _presto

from .handler import Handler as _Handler
from .request import Request as _Request
from .response import Response as _Response

__all__ = "Presto",


class Presto(_presto.Presto):

    class Handler(_Handler):
        pass

    class Request(_Request):
        pass

    class Response(_Response):
        pass

    def __init__(self, url, **kwds):
        super().__init__(
            url=url,
            Handler=self.Handler,
            Request=self.Request,
            Response=self.Response,
            **kwds
        )

    async def __call__(self, url: Optional[str] = None, **kwds) -> Union[Presto, Self, Response]:
        if url is not None:
            presto = copy(self)
            presto.__url__ = url + ("/" if self.APPEND_SLASH and url[-1:] != "/" else "")
            if kwds:
                return await presto.__call__(**kwds)
            return presto

        return await super().__call__(**kwds)
