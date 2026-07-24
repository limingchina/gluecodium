

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional

from smoke.CompressionState import CompressionState
from smoke.Rectangle import Rectangle

from _native_base import _NativeBase

import generated


class UseDartExternalGenerics(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    def use_generics(self, list: list[Rectangle], set: set[CompressionState]) -> dict[CompressionState, Rectangle]:
        """"""
        return _wrap(self._native.use_generics(_unwrap(list, list[Rectangle]), _unwrap(set, set[CompressionState])), dict[CompressionState, Rectangle])

