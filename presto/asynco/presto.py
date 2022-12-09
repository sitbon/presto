from typing import Optional, Type, TypeAlias, TypeVar, Self

from presto import presto

from . import handler, request, response

__all__ = "AsyncPresto",

HandlerT: TypeAlias = TypeVar("HandlerT", bound="AsyncPresto.AsyncHandler")
RequestT: TypeAlias = TypeVar("RequestT", bound="AsyncPresto.AsyncRequest")
ResponseT: TypeAlias = TypeVar("ResponseT", bound="AsyncPresto.AsyncResponse")


# noinspection PyPep8Naming
class AsyncPresto(presto.Presto):

    class AsyncHandler(handler.AsyncHandler):
        pass

    class AsyncRequest(request.AsyncRequest):
        pass

    class AsyncResponse(response.AsyncResponse):
        pass

    # noinspection PyPep8Naming
    def __init__(
            self,
            url: str,
            *,
            Handler: Optional[Type[HandlerT]] = None,
            Request: Optional[Type[RequestT]] = None,
            Response: Optional[Type[ResponseT]] = None,
            **kwds
    ):
        super().__init__(
            url=url,
            Handler=Handler or self.AsyncHandler,
            Request=Request or self.AsyncRequest,
            Response=Response or self.AsyncResponse,
            **kwds
        )

    A: AsyncResponse = presto.Presto.Request.__async__

    def __call__(self, url: Optional[str] = None, **kwds) -> Self:
        if not kwds:
            raise RuntimeError("Use async method by awaiting .A directly.")
        return super().__call__(url=url, **kwds)



