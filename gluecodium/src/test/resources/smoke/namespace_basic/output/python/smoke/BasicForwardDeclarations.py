

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase
from enum import Enum
from typing import Optional
import generated

from smoke.Basic import Basic

class BasicForwardDeclarations(_NativeBase):
    def __init__(self, native):
        super().__init__(native)

    def use_basic(self) -> Basic:
        return _wrap(self._native.use_basic(), Basic)


