from __future__ import annotations

from typing import Type

from presto.adict import adict

from . import presto

__all__ = "PrestoClient",


class PrestoClient:
    """Base class for Presto client API implementations."""

    _APPEND_SLASH: bool = False

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
            Presto: Type[presto.Presto] = presto.Presto,
            Handler: Type[PrestoClient.Handler] = Handler,
            Request: Type[PrestoClient.Request] = Request,
            Response: Type[PrestoClient.Response] = Response,
            APPEND_SLASH: bool = _APPEND_SLASH,
            **kwds
    ):
        if kwds:
            self._params.__merge__(kwds)

        self._presto = Presto(
            url=url,
            Handler=Handler,
            Request=Request,
            Response=Response,
            APPEND_SLASH=APPEND_SLASH,
            **self._params,
        )

    @property
    def url(self):
        return self._presto.__url__
