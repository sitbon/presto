from __future__ import annotations

from typing import Optional, Container, TypeVar

import requests

from presto.adict import adict

__all__ = "Response",

HandlerT = TypeVar("HandlerT", bound="Handler")
RequestT = TypeVar("RequestT", bound="Request")


class Response(requests.Response):
    _RAISE_FOR_STATUS: bool = True
    _RAISE_EXCEPT_FOR: Container = set()

    attr: Optional[adict] = None

    __handler: HandlerT
    __request: RequestT

    def __init__(self, handler: HandlerT, request: RequestT, response: requests.Response):
        self.__handler = handler
        self.__request = request
        self.__dict__ = response.__dict__

        if self._RAISE_FOR_STATUS is True:
            self.raise_for_status()

        if self.status_code == 200 and self.headers.get("content-type").startswith("application/json"):
            self.attr = adict(self.json())

    @property
    def handler(self) -> HandlerT:
        return self.__handler

    @property
    def prequest(self) -> RequestT:
        return self.__request

    def _raise_for_status(self):
        return super().raise_for_status()

    def raise_for_status(self):
        if self.status_code not in self._RAISE_EXCEPT_FOR:
            return self._raise_for_status()
