

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase
from enum import Enum
from typing import Optional
import generated


class InternalPropertyOnly(_NativeBase):
    def __init__(self, native):
        super().__init__(native)

    @property
    def _foo(self) -> str:
        return _wrap(self._native._foo, str)

    @_foo.setter
    def _foo(self, value: str):
        self._native._foo = _unwrap(value, str)


