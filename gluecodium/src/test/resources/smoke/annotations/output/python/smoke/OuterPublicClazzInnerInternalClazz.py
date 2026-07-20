

from __future__ import annotations


from _native_base import _NativeBase

import generated


class OuterPublicClazzInnerInternalClazz(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    def some_function(self) -> bool:
        """"""
        return self._native.some_function()

