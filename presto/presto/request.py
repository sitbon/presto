from abc import ABC, abstractmethod
from typing import Union, Self, Any, TypeVar, Optional, TypeAlias

from copy import copy, deepcopy
from urllib.parse import urljoin

from presto.adict import adict

__all__ = "HandlerT", "RequestT", "ResponseT", "Request"

HandlerT: TypeAlias = TypeVar("HandlerT", bound="__Request__.__Handler__")
RequestT: TypeAlias = TypeVar("RequestT", bound="__Request__")
ResponseT: TypeAlias = TypeVar("ResponseT", bound="__Request__.__Response__")


# noinspection PyPep8Naming
class __Request__(ABC):

    # noinspection PyPep8Naming
    class __Handler__(ABC):
        @abstractmethod
        def __call__(self, requ: RequestT, **kwds) -> ResponseT:
            raise NotImplementedError

    # noinspection PyPep8Naming
    class __Response__(ABC):
        @abstractmethod
        def __init__(self, hand: HandlerT, requ: RequestT, resp: ResponseT):
            raise NotImplementedError

    __handler__: Optional[HandlerT] = None
    __parent__: Optional[RequestT] = None
    __params__: adict
    __requests__: dict[str, RequestT]

    def __init__(self, parent: Optional[RequestT], **kwds):
        self.__handler__ = parent.__handler__ if parent else None
        self.__parent__ = parent if parent else None
        self.__params__ = self.__clean_params__(adict(getattr(self, "__params__", {})).__merged__(kwds))
        self.__requests__ = dict()

    def __repr__(self):
        params = self.__merged__
        url = self.__url__

        if url:
            url = f"url={url!r}"

        if params:
            params = f"{', ' if url else ''}params={params!r}"

        name = self.__class__.__name__

        if name.startswith("_"):
            name = name[1:]

        return f"{name}({url}{params})"

    @property
    @abstractmethod
    def __url__(self) -> Optional[str]:
        raise NotImplementedError

    @property
    def __merged__(self) -> adict:
        if self.__parent__ is None:
            return self.__params__

        return self.__parent__.__merged__.__merged__(self.__params__)

    def __merge__(self, **kwds) -> None:
        self.__params__.__merge__(self.__clean_params__(kwds))

    def __handle__(self) -> ResponseT:
        return self.__handler__(self)

    @property
    async def __async__(self) -> ResponseT:
        return await self.__handler__(self)

    def __getitem__(self, item) -> Self:
        return self.__getattr__(str(item))

    def __getattr__(self, name: str) -> Self:
        if "__" in name:
            raise AttributeError(name)  # Most likely an accidentally invalid internal attribute/method access.

        request = self.__requests__.get(name)

        if request is None:
            request = self.__requests__[name] = self.__handler__.presto.Request(self, name)
        elif request.__parent__ is not self:
            req = copy(request)
            req.__parent__ = self
            request = self.__requests__[name] = req

        return request

    def __call__(self, **kwds) -> Union[Self, ResponseT]:
        if not kwds:
            return self.__handle__()

        self.__merge__(**kwds)
        return self

    def __copy__(self) -> Self:
        this = self.__class__.__new__(self.__class__)
        # this.__url__ = self.__url__  # (Skip "fake abstract" property)
        this.__handler__ = copy(self.__handler__)
        this.__parent__ = self.__parent__
        this.__params__ = self.__params__
        this.__requests__ = self.__requests__
        return this

    def __deepcopy__(self, memo: dict) -> Self:
        this = self.__class__.__new__(self.__class__)
        memo[id(self)] = this
        this.__handler__ = deepcopy(self.__handler__, memo)

        if self.__parent__ is self:
            this.__parent__ = this
        else:
            this.__parent__ = deepcopy(self.__parent__, memo)

        this.__params__ = deepcopy(self.__params__, memo)
        this.__requests__ = deepcopy(self.__requests__, memo)
        return this

    @classmethod
    def __clean_params__(cls, params: Union[adict, dict[str, Any]]) -> Union[adict, dict[str, Any]]:
        if "url" in params:
            raise ValueError("url is a reserved parameter name")

        return params

    def __eq__(self, other) -> bool:
        if not isinstance(other, __Request__):
            return False

        return self.__url__ == other.__url__ and self.__merged__ == other.__merged__


class Request(__Request__):

    __Request__ = __Request__

    __path__: str

    def __init__(self, parent: RequestT, path: str):
        super().__init__(parent)

        if self.__handler__.APPEND_SLASH and not path.endswith("/"):
            path += "/"

        self.__path__ = path

    @property
    def __url__(self) -> str:
        return urljoin(self.__parent__.__url__ + "/", self.__path__)

    def __copy__(self) -> Self:
        this: Self = super().__copy__()
        this.__path__ = self.__path__
        return this

    def __deepcopy__(self, memo: dict) -> Self:
        this: Self = super().__deepcopy__(memo)
        this.__path__ = self.__path__
        return this
