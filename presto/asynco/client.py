from typing import Type, Optional

from presto import client

from . import presto

__all__ = "AsyncPrestoClient",


class AsyncPrestoClient(client.PrestoClient):
    """Base class for Presto client API implementations."""

    _presto: presto.AsyncPresto

    # noinspection PyPep8Naming
    def __init__(
            self,
            url: str,
            *,
            Presto: Optional[Type[presto.AsyncPresto]] = None,
            Handler: Optional[Type[presto.AsyncPresto.AsyncHandler]] = None,
            Request: Optional[Type[presto.AsyncPresto.AsyncRequest]] = None,
            Response: Optional[Type[presto.AsyncPresto.AsyncResponse]] = None,
            **kwds
    ):
        super().__init__(
            url=url,
            Presto=Presto,
            Handler=Handler,
            Request=Request,
            Response=Response,
            **kwds,
        )
