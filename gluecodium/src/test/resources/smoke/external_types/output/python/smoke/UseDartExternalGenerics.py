

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase, _install_callback_adapters, _unwrap_struct_args, _mark_callback_base, _struct_key
from enum import Enum
from typing import Optional
import generated

from smoke.CompressionState import CompressionState
from smoke.Rectangle import Rectangle

class UseDartExternalGenerics(_NativeBase):
    def __init__(self, native):
        super().__init__(native)

    def use_generics(self, list: list[Rectangle], set: set[CompressionState]) -> dict[CompressionState, Rectangle]:
        return _wrap(self._native.use_generics(_unwrap(list, list[Rectangle]), _unwrap(set, set[CompressionState])), dict[CompressionState, Rectangle])
