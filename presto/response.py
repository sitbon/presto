from __future__ import annotations

import requests

from .typing import AttrCopyable
from .adict import adict

__all__ = "Response",


class Response(AttrCopyable, requests.Response):
    __state_attrs__ = requests.Response.__attrs__ + ["attr"]

    def __init__(self, response: requests.Response):
        self.__dict__ = response.__dict__
        self.raise_for_status()

        if self.headers.get("content-type").startswith("application/json"):
            self.attr = adict(self.json())
