import contextlib
import copy
from typing import ClassVar, Self


class Context(contextlib.ContextDecorator):
    stack: ClassVar[list[dict[str, int | float | list | set | dict]]] = [{}]

    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def __enter__(self):
        Context.stack[-1] = {k: o.value for k, o in ContextVar._cache.items()}  # Store current state.
        for k, v in self.kwargs.items():
            ContextVar._cache[k].value = v  # Update to new temporary state.
        Context.stack.append(self.kwargs)  # Store the temporary state so we know what to undo later.

    def __exit__(self, *args):
        for k in Context.stack.pop():
            ContextVar._cache[k].value = Context.stack[-1].get(k, ContextVar._cache[k].value)

    @classmethod
    def get_all(cls):
        return {k: o.value for k, o in ContextVar._cache.items()}


class ContextVar:
    _cache: ClassVar[dict[str, Self]] = {}
    value: int | float | list | set | dict
    key: str

    def __init__(self, key, default_value):
        assert key not in ContextVar._cache, f"attempt to recreate ContextVar {key}"
        ContextVar._cache[key] = self
        self.key = key
        self.value = default_value
        self.default_value = default_value

    def reset(self):
        self.value = self.default_value

    def __bool__(self):
        return bool(self.value)

    def __eq__(self, x):
        return self.value == x

    def __ge__(self, x):
        return self.value >= x

    def __gt__(self, x):
        return self.value > x

    def __lt__(self, x):
        return self.value < x

    def __le__(self, x):
        return self.value <= x

    def __str__(self):
        return str(self.value)

    def __int__(self):
        return int(self.value)  # type: ignore

    def __float__(self):
        return float(self.value)  # type: ignore

    def __add__(self, other):
        return self.value + other

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        return self.value - other

    def __rsub__(self, other):
        return other - self.value

    def __mul__(self, other):
        return self.value * other

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        return self.value / other

    def __rtruediv__(self, other):
        return other / self.value

    def __iter__(self):
        return iter(copy.deepcopy(self.value))  # type: ignore # copy to prevent mutation of the original value

    def __getitem__(self, key):
        return copy.deepcopy(self.value[key])  # type: ignore # copy to prevent mutation of the original value

    def __contains__(self, item) -> bool:
        return item in self.value

    def __len__(self) -> int:
        return len(self.value)  # type: ignore
