

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase
from enum import Enum
from typing import Optional
import generated


class NullableOverloads(_NativeBase):
    def __init__(self, native):
        super().__init__(native)

    def foo(self, *args, **kwargs):
        return _wrap(self._native.foo(*[_unwrap(a) for a in args]), None)



