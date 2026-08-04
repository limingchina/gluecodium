

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase
from enum import Enum
from typing import Optional
import generated


class RenamedClass(_NativeBase):
    def __init__(self, native):
        super().__init__(native)

    def _internal_method(self) -> str:
        return _wrap(self._native._internal_method(), str)

    def visible_method(self, param: int) -> str:
        return _wrap(self._native.visible_method(_unwrap(param, int)), str)


