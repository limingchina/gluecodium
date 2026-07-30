

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper
from typing import Optional

from smoke.MethodOverloadsPoint import MethodOverloadsPoint

from _native_base import _NativeBase

import generated


class MethodOverloads(_NativeBase):
    def __init__(self, native):
        super().__init__(native)

    def is_boolean(*args, **kwargs) -> bool:
        return _wrap(self._native.is_boolean(*[_unwrap(a) for a in args]), bool)








    def is_float(*args, **kwargs) -> bool:
        return _wrap(self._native.is_float(*[_unwrap(a) for a in args]), bool)


