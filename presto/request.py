from __future__ import annotations

from abc import ABC
from typing import Union, Dict, Self, Any, TypeVar, Generic

from urllib.parse import urljoin

from .adict import adict

__all__ = "_Request",

HandlerT = TypeVar("HandlerT", bound="_Handler")
ResponseT = TypeVar("ResponseT", bound="_Response")


class __Request__(Generic[HandlerT], ABC):

    __url__: str = None  # abstract
    __handler__: HandlerT
    __parent__: __Request__[HandlerT]
    __params__: adict
    __requests__: Dict[str, __Request__[HandlerT]]

    def __init__(self, parent: __Request__[HandlerT], **kwds):
        self.__handler__ = parent.__handler__
        self.__parent__ = parent
        self.__params__ = self.__clean_params__(adict(getattr(self, "__params__", {})).merged(kwds))
        self.__requests__ = dict()

    def __repr__(self):
        params = self.__request__
        url = self.__url__

        if self.__url__:
            url = f"url={url!r}"

        if params:
            params = f"{', ' if url else ''}params={params!r}"

        name = self.__class__.__name__

        if name.startswith("_"):
            name = name[1:]

        return f"{name}({url}{params})"

    @classmethod
    def __clean_params__(cls, params: Union[adict, Dict[str, Any]]) -> Union[adict, Dict[str, Any]]:
        if "url" in params:
            raise ValueError("url is a reserved parameter name")

        return params

    def __getattr__(self, name: str) -> __Request__[HandlerT]:
        if name.startswith("__") and name.endswith("__"):
            raise AttributeError(name)  # Most likely an accidentally invalid internal attribute/method access.

        request = self.__requests__.get(name)

        if request is None:
            request = self.__requests__[name] = self.__handler__.Request(self, name)
        elif request.__parent__ is not self:
            if request.__parent__ is not self.__parent__:
                raise AttributeError(f"Request '{name}' has a different parent from this request.")

            req = request.__copy__()
            req.__parent__ = self
            request = self.__requests__[name] = req

        return request

    def __getitem__(self, item) -> __Request__[HandlerT]:
        return self.__getattr__(str(item))

    def __call__(self, **kwds) -> Union[Self, ResponseT]:
        if not kwds:
            return self.__handler__(self)

        self.__params__.merge(self.__clean_params__(kwds))
        return self

    @property
    def __request__(self) -> adict:
        if self.__parent__ is self:
            return self.__params__

        return self.__parent__.__request__.merged(self.__params__)

    # @property
    # @abstractmethod
    # def __url__(self) -> str:
    #     raise NotImplementedError

    def __copy__(self) -> Self:
        this = self.__class__.__new__(self.__class__)
        # this.__url__ = self.__url__  # (Skip "fake abstract" property)
        this.__handler__ = self.__handler__
        this.__parent__ = self.__parent__
        this.__params__ = self.__params__
        this.__requests__ = self.__requests__
        return this

    def __eq__(self, other) -> bool:
        if not isinstance(other, __Request__):
            return False

        return self.__url__ == other.__url__ and self.__request__ == other.__request__


class _Request(__Request__):

    __path__: str

    def __init__(self, parent: __Request__, path: str):
        super().__init__(parent)

        if self.__handler__.APPEND_SLASH and not path.endswith("/"):
            path += "/"

        self.__path__ = path

    def __set__(self, instance, value):
        if isinstance(value, dict):
            self.__params__.merge(value)
        else:
            raise TypeError(f"Cannot set {self.__class__.__name__} with type {type(value)}")
        return self

    @property
    def __url__(self):
        return urljoin(self.__parent__.__url__ + "/", self.__path__)

    def __copy__(self) -> Self:
        this = super().__copy__()
        this.__path__ = self.__path__
        return this
