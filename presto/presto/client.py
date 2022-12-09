from __future__ import annotations

from typing import Type, Optional

from presto.adict import adict

from . import presto

__all__ = "PrestoClient",


class PrestoClient:
    """Base class for Presto client API implementations."""

    _presto: presto.Presto

    _params: adict = adict(
        method="GET",
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
    )

    class Handler(presto.Presto.Handler):
        pass

    class Request(presto.Presto.Request):
        pass

    class Response(presto.Presto.Response):
        pass

    # noinspection PyPep8Naming
    def __init__(
            self,
            url: str,
            *,
            Presto: Optional[Type[presto.Presto]] = None,
            Handler: Optional[Type[PrestoClient.Handler]] = None,
            Request: Optional[Type[PrestoClient.Request]] = None,
            Response: Optional[Type[PrestoClient.Response]] = None,
            **kwds
    ):
        if kwds:
            self._params.__merge__(kwds)

        Presto = Presto or presto.Presto

        self._presto = Presto(
            url=url,
            Handler=Handler or self.Handler,
            Request=Request or self.Request,
            Response=Response or self.Response,
            **self._params,
        )

    @property
    def url(self):
        return self._presto.__url__
