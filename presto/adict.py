from __future__ import annotations

from typing import Union, Iterator

from attrdict import AttrDict

__all__ = "adict",


# noinspection PyPep8Naming
class adict(AttrDict):
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({', '.join(f'{str(key)}={value!r}' for key, value in self.items())})"

    def merge(self: Union[adict, dict], other: dict) -> Union[adict, dict]:
        for key, value in other.items():
            if key in self and isinstance(self[key], dict) and isinstance(value, dict):
                self[key] = adict.merge(self[key], value)
            else:
                self[key] = value

        return self

    def merged(self: Union[adict, dict], other: dict) -> Union[adict, dict]:
        this = adict(self) if isinstance(self, adict) else dict(self)
        return adict.merge(this, other)

    def filter(self: Union[adict, dict], *keys: str, delete=False) -> dict:

        def op(k, v):
            if k in keys and delete:
                del self[k]

            if isinstance(v, (adict, dict)):
                return adict.filter(v, *keys, delete=delete)

            return v

        filtered = {
            key: op(key, val)
            for key, val in tuple(self.items())
        }

        return filtered
