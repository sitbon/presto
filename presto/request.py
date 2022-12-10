from typing import Any, Optional, TypeAlias, Container, Self, Type
from abc import ABC, abstractmethod

from copy import deepcopy, copy
from urllib.parse import urljoin

from presto.adict import adict

__all__ = "Request",

RequestT: TypeAlias = "Request"
HandlerT: TypeAlias = "Request.Handler"


# noinspection PyPep8Naming
class Request(ABC):
    """"""
    APPEND_SLASH: bool = False
    APPEND_SLASH_INHERIT: bool = True

    __parent: Optional[RequestT]
    __handler: HandlerT
    __path: str
    __params: adict
    __requests: dict[str, RequestT]

    Request: Type[RequestT] = NotImplemented

    # noinspection PyPep8Naming
    class Handler(ABC):
        class Response(ABC):
            RAISE_FOR_STATUS: bool = True
            RAISE_EXCEPT_FOR: Container = set()

            __handler: HandlerT
            __request: RequestT

            def __init__(self, hand: HandlerT, requ: RequestT):
                self.__handler = hand
                self.__request = requ
                self.raise_for_status()

            @property
            def handler(self) -> HandlerT:
                return self.__handler

            @property
            def prequest(self) -> RequestT:
                return self.__request

            def _should_raise_for_status(self, status_code: int) -> bool:
                return self.RAISE_FOR_STATUS and status_code not in self.RAISE_EXCEPT_FOR

            @abstractmethod
            def raise_for_status(self):
                raise NotImplementedError

            @property
            @abstractmethod
            def attr(self) -> adict:
                raise NotImplementedError

            def __call__(self) -> adict:
                return self.attr

        @abstractmethod
        def __call__(self, requ: RequestT) -> Response:
            raise NotImplementedError

        async def A(self, requ: RequestT) -> Response:
            return self(requ)

    def __init__(
            self,
            *,
            parent: Optional[RequestT],
            path: str,
            APPEND_SLASH: Optional[bool] = None,
            **kwds
    ):
        self.__parent = parent

        if parent is not None:

            if self.Request is NotImplemented:
                if parent.Request is NotImplemented:
                    raise TypeError("Request.Request must be defined for parent.")

                self.Request = parent.Request
        else:
            if self.Request is NotImplemented:
                raise TypeError("Request.Request must be defined for subclass.")

        self.__handler = self.Request.Handler()

        self.APPEND_SLASH = APPEND_SLASH if APPEND_SLASH is not None else (
            self.APPEND_SLASH if not self.APPEND_SLASH_INHERIT else (parent or self).APPEND_SLASH
        )

        self.__path__ = path

        self.__params = adict(self.__clean_params__(getattr(self, "__params__", {})))
        self.__merge__(**kwds)

        self.__requests = dict()

    def __copy__(self) -> Self:
        this: Self = self.__class__.__new__(self.__class__)
        this.__parent = self.__parent
        this.__handler = self.__handler
        this.__path = self.__path
        this.APPEND_SLASH = self.APPEND_SLASH
        this.__params = self.__params
        this.__requests = self.__requests
        return this

    def __deepcopy__(self, memo: Optional[dict[int, Any]]) -> Self:
        this: Self = self.__copy__()
        this.__parent = deepcopy(self.__parent, memo)
        this.__handler = deepcopy(self.__handler, memo)
        this.__params = deepcopy(self.__params, memo)
        this.__requests = deepcopy(self.__requests, memo)
        return this

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
    def __path__(self) -> str:
        return self.__path

    @__path__.setter
    def __path__(self, path: str):
        self.__path = path + ("/" if self.APPEND_SLASH and path[-1:] != "/" else "")

    @property
    def __url__(self) -> str:
        if self.__parent is None:
            return self.__path

        return urljoin(self.__parent.__url__ + "/", self.__path)

    @property
    def __merged__(self) -> adict:
        if self.__parent is None:
            return self.__params

        return self.__parent.__merged__.__merged__(self.__params)

    def __merge__(self, **kwds) -> None:
        self.__params.__merge__(self.__clean_params__(kwds))

    def __handle__(self) -> Handler.Response:
        return self.__handler(deepcopy(self))

    @property
    async def A(self):
        return await self.__handler.A(self)

    def __getitem__(self, item: Any) -> Self:
        return self.__getattr__(str(item))

    def __getattr__(self, name: str) -> Self:
        if "__" in name:
            raise AttributeError(name)  # Most likely an accidentally invalid internal attribute/method access.

        if (request := self.__requests.get(name)) is None:
            request = self.__requests[name] = self.Request(parent=self, path=name)

        elif request.__parent is not self:
            req = copy(request)
            req.__parent = self
            request = self.__requests[name] = req

        return request

    def __call__(self, **kwds) -> Self | Handler.Response:
        if not kwds:
            return self.__handle__()

        self.__merge__(**kwds)
        return self

    @classmethod
    def __clean_params__(cls, params: adict | dict) -> adict | dict:
        if "url" in params:
            raise ValueError("url is a reserved request attribute.")

        return params

    def __eq__(self, other) -> bool:
        if not isinstance(other, self.__class__):
            return False

        return self.__url__ == other.__url__ and self.__merged__ == other.__merged__
