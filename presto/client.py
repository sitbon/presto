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

    # noinspection PyPep8Naming
    def __init__(
            self,
            url: str,
            *,
            Presto: Optional[Type[presto.Presto]] = None,
            Handler: Optional[Type[presto.Presto.Handler]] = None,
            Request: Optional[Type[presto.Presto.Request]] = None,
            Response: Optional[Type[presto.Presto.Response]] = None,
            **kwds
    ):
        if kwds:
            self._params.__merge__(kwds)

        Presto = Presto or presto.Presto

        self._presto = Presto(
            url=url,
            Handler=Handler,
            Request=Request,
            Response=Response,
            **self._params,
        )

    @property
    def url(self):
        return self._presto.__url__
