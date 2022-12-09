from __future__ import annotations

from typing import Type, Optional

from presto.presto import client

from . import presto

__all__ = "AsyncPrestoClient",


class AsyncPrestoClient(client.PrestoClient):
    """Base class for Presto client API implementations."""

    _presto: presto.AsyncPresto

    class AsyncHandler(presto.AsyncPresto.Handler):
        """Placeholder for readability."""

    class AsyncRequest(presto.AsyncPresto.Request):
        """Placeholder for readability."""

    class AsyncResponse(presto.AsyncPresto.Response):
        """Placeholder for readability."""

    # noinspection PyPep8Naming
    def __init__(
            self,
            url: str,
            *,
            Presto: Optional[Type[presto.AsyncPresto]] = None,
            Handler: Optional[Type[AsyncPrestoClient.AsyncHandler]] = None,
            Request: Optional[Type[AsyncPrestoClient.AsyncRequest]] = None,
            Response: Optional[Type[AsyncPrestoClient.AsyncResponse]] = None,
            **kwds
    ):
        super().__init__(
            url=url,
            Presto=Presto or presto.AsyncPresto,
            Handler=Handler or self.AsyncHandler,
            Request=Request or self.AsyncRequest,
            Response=Response or self.AsyncResponse,
            **kwds,
        )

    @property
    def url(self):
        return self._presto.__url__
