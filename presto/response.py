from typing import Optional, Container, TypeVar, TypeAlias

import requests

from presto.adict import adict

from . import request

__all__ = "Response",


class Response(requests.Response, request.Request.__Response__):
    _RAISE_FOR_STATUS: bool = True
    _RAISE_EXCEPT_FOR: Container = set()

    _attr: Optional[adict] = None

    __handler: request.HandlerT
    __request: request.Request

    def __init__(self, hand: request.HandlerT, requ: request.Request, resp: requests.Response):
        self.__handler = hand
        self.__request = requ
        self.__dict__ = resp.__dict__

        if self._RAISE_FOR_STATUS is True:
            self.raise_for_status()

    @property
    def attr(self) -> adict:
        if self._attr is None:
            if self.status_code == 200 and self.headers.get("content-type").startswith("application/json"):
                self._attr = adict(self.json())
        return self._attr

    @property
    def handler(self) -> request.HandlerT:
        return self.__handler

    @property
    def prequest(self) -> request.Request:
        return self.__request

    def _raise_for_status(self):
        return super().raise_for_status()

    def raise_for_status(self):
        if self.status_code not in self._RAISE_EXCEPT_FOR:
            return self._raise_for_status()
