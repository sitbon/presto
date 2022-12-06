from .presto import Presto


class PrestoClient:
    """Template class for Presto client API implementations."""
    _APPEND_SLASH: bool = False
    _presto: Presto
    _params: dict = dict(
        method="GET",
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
    )

    class Handler(Presto.Handler):
        """Placeholder for readability."""
        pass

    class Request(Presto.Request):
        """Placeholder for readability."""
        pass

    class Response(Presto.Response):
        """Placeholder for readability."""
        pass

    def __init__(self, url: str):
        self._presto = Presto(
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
