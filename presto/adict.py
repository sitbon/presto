from typing import Any, TypeAlias, TypeVar

from attrdict import AttrDict

__all__ = "Adict", "adict",

Adict: TypeAlias = "adict | dict"
AdictSelf = TypeVar("AdictSelf", "adict", "dict")


# noinspection PyPep8Naming
class adict(AttrDict):
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({', '.join(f'{str(key)}={value!r}' for key, value in self.items())})"

    def __merge__(self: AdictSelf, other: Adict) -> AdictSelf:
        for key, value in other.items():
            if key in self and isinstance(self[key], dict) and isinstance(value, dict):
                self[key] = adict.__merge__(self[key], value)
            else:
                self[key] = value

        return self

    def __merged__(self: AdictSelf, other: Adict) -> AdictSelf:
        this: AdictSelf = adict(self) if isinstance(self, adict) else dict(self)
        return adict.__merge__(this, other)

    def __delitem__(self: AdictSelf, key: Any) -> None:

        for key, val in tuple(self.items()):
            if isinstance(val, (adict, dict)):
                adict.__delitem__(val, key)

            super().__delitem__(key)
