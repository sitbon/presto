from __future__ import annotations

from typing import Optional

import requests

from .adict import adict

__all__ = "_Response",


class _Response(requests.Response):
    attr: Optional[adict] = None

    # noinspection PyMissingConstructor
    def __init__(self, response: requests.Response):
        self.__dict__ = response.__dict__
        self.raise_for_status()

        if self.ok and self.headers.get("content-type").startswith("application/json"):
            self.attr = adict(self.json())
