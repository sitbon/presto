from . import presto, client

__all__ = "Presto", "PrestoClient"


class Presto(presto.Presto):
    pass


class PrestoClient(client.PrestoClient):
    pass
