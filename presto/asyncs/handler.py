import httpx

from presto.adict import adict
from presto.presto import Presto

from .response import Response

__all__ = "Handler",


class Handler(Presto.Handler):

    async def __call__(self, request: Presto.Request, **kwds) -> Presto.Response:
        url = request.__url__
        params = adict(request.__request__).__merge__(kwds)
        method = params.pop("method")
        async with httpx.AsyncClient() as client:
            return Response(await client.request(method, url, **params))
