from typing import Self, Any, TypeVar, Optional, TypeAlias, Container
from abc import ABC, abstractmethod

from copy import deepcopy, copy
from urllib.parse import urljoin

from presto.adict import adict

__all__ = "Request",

RequestT: TypeAlias = TypeVar("RequestT", bound="Request")
HandlerT: TypeAlias = TypeVar("HandlerT", bound="Request.Handler")


# noinspection PyPep8Naming
class Request(ABC):
    """"""
    APPEND_SLASH: bool = False

    __parent: Optional[RequestT] = None
    __handler: HandlerT = None
    __path: Optional[str] = None
    __params: adict
    __requests: dict[str, RequestT]

    Request: RequestT = NotImplemented

    # noinspection PyPep8Naming
    class Handler(ABC):
        class Response(ABC):
            _RAISE_FOR_STATUS: bool = True
            _RAISE_EXCEPT_FOR: Container = set()

            __handler: HandlerT
            __request: RequestT

            def __init__(self, hand: HandlerT, requ: RequestT):
                self.__handler = hand
                self.__request = requ
                self._raise_for_status()

            @property
            def handler(self) -> HandlerT:
                return self.__handler

            @property
            def prequest(self) -> RequestT:
                return self.__request

            def _should_raise_for_status(self, status_code: int) -> bool:
                return self._RAISE_FOR_STATUS and status_code not in self._RAISE_EXCEPT_FOR

            @abstractmethod
            def _raise_for_status(self):
                raise NotImplementedError

            @property
            @abstractmethod
            def attr(self) -> adict:
                raise NotImplementedError

        @abstractmethod
        def __call__(self, requ: RequestT) -> Response:
            raise NotImplementedError

        async def A(self, requ: RequestT) -> Response:
            return self(requ)

    def __init__(
            self,
            parent: Optional[RequestT],
            path: Optional[str] = None,
            APPEND_SLASH: Optional[bool] = None,
            **kwds
    ):
        if parent is not None:
            self.__parent = parent

            if self.Request is NotImplemented:
                if parent.Request is NotImplemented:
                    raise TypeError("Request.Request must be defined for parent.")

                self.Request = parent.Request
        else:
            if self.Request is NotImplemented:
                raise TypeError("Request.Request must be defined for subclass.")

        self.__handler = self.Request.Handler()

        self.APPEND_SLASH = APPEND_SLASH if APPEND_SLASH is not None else self.APPEND_SLASH
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
    def __path__(self) -> Optional[str]:
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

    def __getitem__(self, item) -> Self:
        return self.__getattr__(str(item))

    def __getattr__(self, name: str) -> Self:
        if "__" in name:
            raise AttributeError(name)  # Most likely an accidentally invalid internal attribute/method access.

        if (request := self.__requests.get(name)) is None:
            request = self.__requests[name] = self.Request(
                parent=self,
                path=name,
                APPEND_SLASH=self.APPEND_SLASH
            )

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
        if not isinstance(other, Request):
            return False

        return self.__url__ == other.__url__ and self.__merged__ == other.__merged__
