

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase
from enum import Enum
from typing import Optional
import generated


class SimpleClass(_NativeBase):
    def __init__(self, native):
        super().__init__(native)

    def get_string_value(self) -> str:
        return _wrap(self._native.get_string_value(), str)

    def use_simple_class(self, input: SimpleClass) -> SimpleClass:
        return _wrap(self._native.use_simple_class(_unwrap(input, SimpleClass)), SimpleClass)


