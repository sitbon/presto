from typing import Self, TypeVar, Union, Optional

from presto import presto

__all__ = "AsyncRequest",

PrestoT = TypeVar("PrestoT", bound="AsyncPresto")
ResponseT = TypeVar("ResponseT", bound="AsyncResponse")


class AsyncRequest(presto.Presto.Request):

    A: ResponseT = presto.Presto.Request.__async__

    def __call__(self, **kwds) -> Union[Self, ResponseT]:
        if not kwds:
            raise RuntimeError("Use async method by awating .A directly.")
        return super().__call__(**kwds)

