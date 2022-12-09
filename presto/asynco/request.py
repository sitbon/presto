from typing import Self, TypeVar, Union, TypeAlias

from presto import presto

__all__ = "AsyncRequest",

HandlerT: TypeAlias = TypeVar("HandlerT", bound="AsyncRequest.__Handler__")
RequestT: TypeAlias = TypeVar("RequestT", bound="AsyncRequest")
ResponseT: TypeAlias = TypeVar("ResponseT", bound="AsyncRequest.__Response__")


class AsyncRequest(presto.Presto.Request):

    # noinspection PyPep8Naming
    class __Handler__(presto.Presto.Handler):
        pass

    # noinspection PyPep8Naming
    class __Response__(presto.Presto.Response):
        pass

    A: ResponseT = presto.Presto.Request.__async__

    def __call__(self, **kwds) -> Union[Self, ResponseT]:
        if not kwds:
            raise RuntimeError("Use async method by awating .A directly.")
        return super().__call__(**kwds)
