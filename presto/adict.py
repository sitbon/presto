from typing import Any, Self

from attrdict import AttrDict
from copy import deepcopy

__all__ = "adict",


# noinspection PyPep8Naming
class adict(AttrDict):
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({', '.join(f'{str(key)}={value!r}' for key, value in self.items())})"

    def __merge__(self, other: dict) -> Self:
        for key, value in other.items():
            if isinstance(value, dict) and key in self and isinstance(self_key := self[key], dict):
                self[key] = adict.__merge__(self_key, value)
            else:
                self[key] = value

        return self

    def __merged__(self, other: dict) -> Self:
        return adict.__merge__(deepcopy(self), other)

    def __delitem__(self, key: Any) -> None:

        for key, val in tuple(self.items()):
            if isinstance(val, (adict, dict)):
                adict.__delitem__(val, key)

            super().__delitem__(key)

    @classmethod
    def __from_json__(cls, json: Any) -> Self | list[Self] | Any:
        if isinstance(json, dict):
            return cls((key, cls.__from_json__(value)) for key, value in json.items())

        if isinstance(json, list):
            return [cls.__from_json__(item) for item in json]

        return json
