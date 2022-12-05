from __future__ import annotations

from typing import TypeVar, Generic, Dict, Any, Type, Union, Optional
from abc import ABC, abstractmethod

import sys
import importlib
from copy import copy

from deepdiff import DeepDiff

__all__ = "Serializable",

T = TypeVar("T")

TYPE_KEY = "__type__"
DATA_KEY = "__data__"


class Serializable(Generic[T], ABC):

    @classmethod
    def __class_getstate__(cls) -> Dict[str, Union[str, Optional[T]]]:
        return {
            TYPE_KEY: cls.__module__ + "." + cls.__name__,
            DATA_KEY: None,
        }

    def __getstate__(self, memo: Optional[Dict] = None) -> Dict[str, Union[str, Optional[T]]]:
        return {
            **self.__class_getstate__(),
            DATA_KEY: self.__get_state__(memo)
        }

    def __setstate__(self, state: Dict[str, Union[str, Optional[T]]], memo: Optional[Dict] = None):
        if DATA_KEY not in state:
            raise ValueError("Invalid state: Missing '__data__' key.")

        for attr, value in self.__class_getstate__().items():
            if attr not in state or state[attr] != value:
                raise ValueError(f"Invalid state: Type mismatch. {state[attr]} != {value}")

        return self.__set_state__(state[DATA_KEY], memo)

    @staticmethod
    def __fromstate__(state: Dict[str, Union[str, T]], memo: Optional[Dict] = None) -> Union[Serializable[T], Type[Serializable[T]]]:

        if DATA_KEY not in state:
            raise ValueError("Invalid state: Missing '__data__' key.")

        if TYPE_KEY not in state:
            raise ValueError("Invalid state: Missing '__type__' key.")

        if state[DATA_KEY] is not None and id(state[DATA_KEY]) in memo:
            return memo[id(state[DATA_KEY])]  # also checked again in __from_state__

        module_name, class_name = state[TYPE_KEY].rsplit(".", 1)

        module = sys.modules[module_name] if module_name in sys.modules else importlib.import_module(module_name)

        cls = getattr(module, class_name)

        if not issubclass(cls, Serializable):
            raise TypeError(f"Class {cls} is not a subclass of Serializable.")

        memo = memo or {}

        if state[DATA_KEY] is None:
            memo[id(state)] = cls
            return cls

        return cls.__from_state__(state[DATA_KEY], memo)

    @abstractmethod
    def __get_state__(self, memo: Optional[Dict] = None) -> T:
        raise NotImplementedError

    @abstractmethod
    def __set_state__(self, state: T, memo: Optional[Dict] = None) -> None:
        raise NotImplementedError

    @classmethod
    def __from_state__(cls, state: T, memo: Optional[Dict] = None) -> Serializable[T]:
        memo = memo or {}

        if id(state) in memo:
            return memo[id(state)]

        memo[id(state)] = this = cls.__new__(cls)
        this.__set_state__(state, memo)
        return this

    def __deepgetstate__(self, obj: Any, memo: Optional[Dict] = None) -> Any:
        memo = memo or {}

        if id(obj) in memo:
            return memo[id(obj)]

        elif isinstance(obj, Serializable) or (isinstance(obj, type) and issubclass(obj, Serializable)):
            if isinstance(obj, type):
                state = obj.__class_getstate__()
            else:
                state = obj.__getstate__(memo)

            memo[id(obj)] = state

        elif isinstance(obj, (list, tuple)):
            state = type(obj)() if isinstance(obj, list) else list(type(obj)())

            memo[id(obj)] = state

            for item in obj:
                state.append(self.__deepgetstate__(item, memo))

        elif isinstance(obj, dict) and set(obj.keys()) == {TYPE_KEY, DATA_KEY}:
            memo[id(obj)] = state = obj

        elif isinstance(obj, dict):
            state = type(obj)()

            memo[id(obj)] = state

            for key, value in obj.items():
                key = self.__deepgetstate__(key, memo)
                state[key] = self.__deepgetstate__(value, memo)

        else:
            memo[id(obj)] = state = copy(obj)

        return state

    def __deepsetstate__(self, state: Any, memo: Optional[Dict] = None) -> Optional[Any]:
        nil = memo is None
        memo = memo or {}

        if id(state) in memo:
            return memo[id(state)]

        if isinstance(state, dict) and set(state.keys()) == {TYPE_KEY, DATA_KEY}:
            setstate = Serializable.__fromstate__(state, memo)

        elif isinstance(state, (list, tuple)):
            setstate = []

            memo[id(state)] = setstate

            for item in state:
                setstate.append(self.__deepsetstate__(item, memo))

        elif isinstance(state, dict):
            setstate = type(state)()

            memo[id(state)] = setstate

            for key, value in state.items():
                key = self.__deepsetstate__(key, memo)
                setstate[key] = self.__deepsetstate__(value, memo)

        else:
            setstate = state

            memo[id(state)] = setstate

        if not nil:
            return setstate

        self.__set_state__(setstate, memo)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Serializable):
            return False

        if other is self:
            return True

        return not DeepDiff(self.__getstate__(), other.__getstate__(), ignore_order=True, max_diffs=1)

    def __ne__(self, other: Any) -> bool:
        return not self.__eq__(other)
