from __future__ import annotations

from typing import TypeVar, Generic, Dict, Self
from abc import ABC

from copy import deepcopy

from .serializable import Serializable

__all__ = "Copyable",

T = TypeVar("T")


class Copyable(Generic[T], Serializable[T], ABC):
    def __copy__(self) -> Self:
        return self.__from_state__(self.__get_state__())

    def __deepcopy__(self, memo: Dict) -> Self:
        return self.__from_state__(deepcopy(self.__get_state__(memo)), memo)
