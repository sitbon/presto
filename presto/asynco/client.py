from .presto import AsyncPresto

from presto.presto.client import PrestoClient

__all__ = "AsyncPrestoClient",


class AsyncPrestoClient(PrestoClient):
    """Template class for Presto client API implementations."""
    
    class Handler(PrestoClient.Handler):
        """Placeholder for readability."""

    class Request(PrestoClient.Request):
        """Placeholder for readability."""

    class Response(PrestoClient.Response):
        """Placeholder for readability."""

    # noinspection PyMissingConstructor
    def __init__(self, url: str):
        self._presto = AsyncPresto(
            url=url,
            Handler=self.Handler,
            Request=self.Request,
            Response=self.Response,
            APPEND_SLASH=self._APPEND_SLASH,
            **self._params
        )

    @property
    def url(self):
        return self._presto.__url__
