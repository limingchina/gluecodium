

from __future__ import annotations

from smoke.StructNestedInInternalStruct import StructNestedInInternalStruct


from _native_base import _NativeBase

import generated


class OuterStructWithInternalAttribute(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], OuterStructWithInternalAttribute):
            super().__init__(args[0])
        else:
            super().__init__(generated.OuterStructWithInternalAttribute(*args))


    @property
    def inner(self) -> StructNestedInInternalStruct:
        """"""
        return self._native.inner

    @inner.setter
    def inner(self, value: StructNestedInInternalStruct):
        self._native.inner = value


