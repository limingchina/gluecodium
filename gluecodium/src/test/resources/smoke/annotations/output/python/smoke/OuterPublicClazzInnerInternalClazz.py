

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper
from typing import Optional


from _native_base import _NativeBase

import generated


class OuterPublicClazzInnerInternalClazz(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    def some_function(self) -> bool:
        """"""
        return _wrap(self._native.some_function(), bool)

