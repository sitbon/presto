from typing import Self, TypeVar, Union

from presto import presto

__all__ = "AsyncRequest",

ResponseT = TypeVar("ResponseT", bound="AsyncResponse")


class AsyncRequest(presto.Presto.Request):

    async def __call__(self, **kwds) -> Union[Self, ResponseT]:
        if not kwds:
            return await self.__handler__(self)

        self.__params__.__merge__(self.__clean_params__(kwds))
        return self
