

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper
from typing import Optional


from _native_base import _NativeBase

import generated


class SpecialAttributes(_NativeBase):
    def __init__(self, native):
        super().__init__(native)

    def with_escaping(self):
        return _wrap(self._native.with_escaping(), None)

    def with_line_break(self):
        return _wrap(self._native.with_line_break(), None)

