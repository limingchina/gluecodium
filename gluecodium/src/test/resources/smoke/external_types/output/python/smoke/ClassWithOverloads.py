

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase
from enum import Enum
from typing import Optional
import generated


class ClassWithOverloads(_NativeBase):
    def __init__(self, native):
        super().__init__(native)

    def one_overload_not_exposed(self) -> str:
        return _wrap(self._native.one_overload_not_exposed(), str)

    def all_overloads_exposed(*args, **kwargs) -> str:
        return _wrap(self._native.all_overloads_exposed(*[_unwrap(a) for a in args]), str)




