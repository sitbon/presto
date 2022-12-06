from __future__ import annotations

from abc import ABC
from typing import Union, Dict, Self, Any, TypeVar, Generic

from urllib.parse import urljoin

from .adict import adict

__all__ = "_Request",

HandlerT = TypeVar("HandlerT", bound="_Handler")
ResponseT = TypeVar("ResponseT", bound="_Response")


class __Request(Generic[HandlerT], ABC):

    __url__: str = None  # abstract
    __handler__: HandlerT
    __parent__: __Request[HandlerT]
    __params__: adict
    __requests__: Dict[str, __Request[HandlerT]]

    def __init__(self, parent: __Request[HandlerT], **kwds):
        self.__handler__ = parent.__handler__
        self.__parent__ = parent
        self.__params__ = self.__clean_params__(adict(getattr(self, "__params__", {})).merged(kwds))
        self.__requests__ = dict()

    @classmethod
    def __clean_params__(cls, params: Union[adict, Dict[str, Any]]) -> Union[adict, Dict[str, Any]]:
        if "url" in params:
            raise ValueError("url is a reserved parameter name")

        return params

    def __getattr__(self, name: str) -> __Request[HandlerT]:
        if name.startswith("__") and name.endswith("__"):
            raise AttributeError(name)  # Most likely an accidentally invalid internal attribute/method access.

        request = self.__requests__.get(name)

        if request is None:
            request = self.__requests__[name] = self.__handler__.Request(self, name)
        elif request.__parent__ is not self:
            if request.__parent__ is not self.__parent__:
                raise AttributeError(f"Request '{name}' has a different parent from this request.")

            req = request.copy()
            req.__parent__ = self
            request = self.__requests__[name] = req

        return request

    def __getitem__(self, item):
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

    def copy(self) -> Self:
        this = self.__class__.__new__(self.__class__)
        # this.__url__ = self.__url__  # (Skip "fake abstract" property)
        this.__handler__ = self.__handler__
        this.__parent__ = self.__parent__
        this.__params__ = self.__params__
        this.__requests__ = self.__requests__
        return this


class _Request(__Request):

    __path__: str

    def __init__(self, parent: __Request, path: str):
        super().__init__(parent)

        if not isinstance(self.__parent__, _Request):
            if not path.startswith("/"):
                path = "/" + path
        elif path.startswith("/"):
            path = path[1:]

        if self.__handler__.APPEND_SLASH and not path.endswith("/"):
            path += "/"

        self.__path__ = path

    def __repr__(self):
        params = ""

        if self.__params__:
            params = f", params={self.__params__!r}"

        return f"{self.__parent__!r}.{self.__class__.__name__.strip('_')}(path={self.__path__!r}{params})"

    def __set__(self, instance, value):
        if isinstance(value, dict):
            self.__params__.merge(value)
        else:
            raise TypeError(f"Cannot set {self.__class__.__name__} with type {type(value)}")
        return self

    @property
    def __url__(self):
        return urljoin(self.__parent__.__url__ + "/", self.__path__)

    def copy(self) -> Self:
        this = super().copy()
        this.__path__ = self.__path__
        return this
