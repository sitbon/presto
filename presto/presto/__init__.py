from . import presto as _presto
from . import client as _client

__all__ = "Presto", "PrestoClient"


class Presto(_presto.Presto):
    pass


class PrestoClient(_client.PrestoClient):
    pass
