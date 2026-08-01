

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase
from enum import Enum
from typing import Optional
import generated


class SwiftMethodOverloads(_NativeBase):
    def __init__(self, native):
        super().__init__(native)

    def one(self, input: str):
        return _wrap(self._native.one(_unwrap(input, str)), None)

    def two(self, input: list[str]):
        return _wrap(self._native.two(_unwrap(input, list[str])), None)


