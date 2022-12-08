from __future__ import annotations

from typing import Optional, Container

import requests

from .adict import adict

__all__ = "_Response",


class _Response(requests.Response):
    _RAISE_FOR_STATUS: bool = True
    _RAISE_EXCEPT_FOR: Container = set()

    attr: Optional[adict] = None

    # noinspection PyMissingConstructor
    def __init__(self, response: requests.Response):
        self.__dict__ = response.__dict__

        if self._RAISE_FOR_STATUS is True:
            self.raise_for_status()

        if self.ok and self.headers.get("content-type").startswith("application/json"):
            self.attr = adict(self.json())

    def _raise_for_status(self):
        return super().raise_for_status()

    def raise_for_status(self):
        if self.status_code not in self._RAISE_EXCEPT_FOR:
            self._raise_for_status()
