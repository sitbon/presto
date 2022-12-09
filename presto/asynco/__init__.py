from . import presto, client

__all__ = "AsyncPresto", "AsyncPrestoClient"


class AsyncPresto(presto.AsyncPresto):
    pass


class AsyncPrestoClient(client.AsyncPrestoClient):
    pass
