from __future__ import annotations

from typing import Any, Dict, Optional, Sequence
from abc import ABC, abstractmethod

from itertools import chain

from deepdiff import DeepDiff

from .serializable import Serializable
from .copyable import Copyable

__all__ = "AttrSerializable", "AttrCopyable"


class AttrSerializable(Serializable[Dict[str, Any]], ABC):

    @classmethod
    def __init_subclass__(cls, **kwargs):
        seen = set()

        if hasattr(cls, "__state_attrs__") and cls.__state_attrs__ is not AttrSerializable.__state_attrs__:
            # noinspection PyPropertyAccess
            cls.__state_attrs__ = tuple(chain(*(
                (attr for attr in getattr(sup, "__state_attrs__", ()) if not (attr in seen or seen.add(attr)))
                for sup in reversed(cls.mro())
                if issubclass(sup, AttrSerializable) and hasattr(sup, "__state_attrs__")
                and sup.__state_attrs__ is not AttrSerializable.__state_attrs__
            )))

        super().__init_subclass__(**kwargs)

    @property
    @abstractmethod
    def __state_attrs__(self) -> Sequence[str]:
        raise NotImplementedError

    def __get_state__(self, memo: Optional[Dict] = None) -> Dict[str, Any]:
        state = {}
        memo = memo or {}
        sid = id(self)

        if sid in memo:
            return memo[sid]

        memo[sid] = state

        for key in self.__state_attrs__:
            attr = getattr(self, key)
            state[key] = self.__deepgetstate__(attr, memo)

        return state

    def __set_state__(self, state: Dict[str, Any], memo: Optional[Dict] = None) -> None:
        if set(state.keys()) != set(self.__state_attrs__):
            raise ValueError("Invalid state.")

        memo = memo or {}

        for key, value in state.items():
            value = self.__deepsetstate__(value, memo)
            setattr(self, str(key), value)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, AttrSerializable):
            return False

        if other is self:
            return True

        for key in self.__state_attrs__:
            if DeepDiff(getattr(self, key), getattr(other, key), ignore_order=True, max_diffs=1):
                return False

        return True

    def __ne__(self, other: Any) -> bool:
        return not self.__eq__(other)


class AttrCopyable(AttrSerializable, Copyable[Dict], ABC):
    pass
