from .presto import AsyncPresto as Presto
from .client import AsyncPrestoClient as PrestoClient

__all__ = "AsyncPresto", "AsyncPrestoClient"


class AsyncPresto(Presto):
    pass


class AsyncPrestoClient(PrestoClient):
    pass
