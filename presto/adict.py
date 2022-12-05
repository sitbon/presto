from __future__ import annotations

from typing import Union

from attrdict import AttrDict

__all__ = "adict",


# noinspection PyPep8Naming
class adict(AttrDict):
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({', '.join(f'{str(key)}={value!r}' for key, value in self.items())})"

    def merged(self: Union[adict, dict], other: dict) -> adict:
        this = adict(self) if isinstance(self, adict) else dict(self)

        for key, value in other.items():
            if key in this and isinstance(this[key], dict) and isinstance(value, dict):
                this[key] = adict.merged(this[key], value)
            else:
                this[key] = value

        return this

    def merge(self, other: dict) -> None:
        self.update(self.merged(other))
