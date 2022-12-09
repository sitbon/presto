from __future__ import annotations

from typing import Type

from presto.presto import client

from .presto import AsyncPresto

__all__ = "AsyncPrestoClient",


class AsyncPrestoClient(client.PrestoClient):
    """Base class for Presto client API implementations."""

    _presto: AsyncPresto

    class Handler(AsyncPresto.Handler):
        """Placeholder for readability."""

    class Request(AsyncPresto.Request):
        """Placeholder for readability."""

    class Response(AsyncPresto.Response):
        """Placeholder for readability."""

    # noinspection PyPep8Naming
    def __init__(
            self,
            url: str,
            *,
            Handler: Type[AsyncPrestoClient.Handler] = Handler,
            Request: Type[AsyncPrestoClient.Request] = Request,
            Response: Type[AsyncPrestoClient.Response] = Response,
            APPEND_SLASH: bool = client.PrestoClient._APPEND_SLASH,
            **kwds
    ):
        super().__init__(
            url=url,
            Presto=AsyncPresto,
            Handler=Handler,
            Request=Request,
            Response=Response,
            APPEND_SLASH=APPEND_SLASH,
            **kwds,
        )

    @property
    def url(self):
        return self._presto.__url__
