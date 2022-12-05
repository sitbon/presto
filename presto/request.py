from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional, Union, Dict, Self, Any, TypeVar

from urllib.parse import urljoin

from deepdiff import DeepDiff

from .typing import AttrCopyable
from .adict import adict

__all__ = "Request",

THandler = TypeVar("THandler", bound="Handler")
TResponse = TypeVar("TResponse", bound="Response")


class AbstractRequest(AttrCopyable, ABC):
    __state_attrs__ = "__handler__", "__parent__", "__params__", "__requests__"

    __handler__: THandler
    __parent__: Request
    __params__: adict
    __requests__: Dict[str, AbstractRequest]

    def __init__(self, parent: AbstractRequest, **kwds):
        self.__handler__ = parent.__handler__
        self.__parent__ = parent
        self.__params__ = self.__clean_params__(adict(getattr(self, "__params__", {})).merged(kwds))
        self.__requests__ = dict()

    @classmethod
    def __clean_params__(cls, params: Union[adict, Dict[str, Any]]) -> Union[adict, Dict[str, Any]]:
        if "url" in params:
            raise ValueError("url is a reserved parameter name")

        return params

    def __getattr__(self, name: str) -> AbstractRequest:
        if name.startswith("__") and name.endswith("__"):
            raise AttributeError(name)

        request = self.__requests__.get(name)

        if request is None:
            request = self.__requests__[name] = self.__handler__.Request(self, name)
        elif request.__parent__ is not self:
            if request.__parent__ is not self.__parent__:
                raise AttributeError(f"Request '{name}' has a different parent from this request.")

            req = request.__copy__()
            req.__handler__ = self.__handler__
            req.__parent__ = self
            req.__params__ = request.__params__
            req.__requests__ = request.__requests__
            request = self.__requests__[name] = req

        return request

    def __getitem__(self, item):
        return self.__getattr__(str(item))

    def __call__(self, **kwds) -> Union[Self, TResponse]:
        if not kwds:
            return self.__handler__(self)

        self.__params__.merge(self.__clean_params__(kwds))
        return self

    @property
    def __request__(self) -> adict:
        if self.__parent__ is self:
            return self.__params__

        return self.__parent__.__request__.merged(self.__params__)

    @property
    @abstractmethod
    def __url__(self) -> str:
        raise NotImplementedError

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, AbstractRequest):
            return False

        if other is self:
            return True

        return \
            self.__handler__ == other.__handler__ and \
            not DeepDiff(self.__params__, other.__params__, ignore_order=True, max_diffs=1) and \
            self.__url__ == other.__url__
        # ...
        # and not DeepDiff(self.__requests__, other.__requests__, ignore_order=True, max_diffs=1)


class Request(AbstractRequest):
    __state_attrs__ = "__path__",

    __path__: str

    def __init__(self, parent: AbstractRequest, path: str):
        super().__init__(parent)

        if self.__parent__ is self.__handler__.presto:
            if not path.startswith("/"):
                path = "/" + path
        elif path.startswith("/"):
            path = path[1:]

        if self.__handler__.presto.APPEND_SLASH and not path.endswith("/"):
            path += "/"

        self.__path__ = path

    def __repr__(self):
        params = ""

        if self.__params__:
            params = f", params={self.__params__!r}"

        return f"{self.__parent__!r}.{self.__class__.__name__}(path={self.__path__!r}{params})"

    def __set__(self, instance, value):
        if isinstance(value, dict):
            self.__params__.merge(value)
        else:
            raise TypeError(f"Cannot set {self.__class__.__name__} with type {type(value)}")
        return self

    @property
    def __url__(self):
        return urljoin(self.__parent__.__url__ + "/", self.__path__)
