

from smoke.OuterStructWithInternalAttributeStructNestedInInternalStruct import OuterStructWithInternalAttributeStructNestedInInternalStruct
import typing


from _native_base import _NativeBase

import generated


class OuterStructWithInternalAttribute(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.OuterStructWithInternalAttribute):
            super().__init__(args[0])
        else:
            super().__init__(generated.OuterStructWithInternalAttribute(*[_unwrap(arg) for arg in args]))


    @property
    def inner(self) -> OuterStructWithInternalAttributeStructNestedInInternalStruct:
        """"""
        return _wrap(self._native.inner, OuterStructWithInternalAttributeStructNestedInInternalStruct)
    @inner.setter
    def inner(self, value: OuterStructWithInternalAttributeStructNestedInInternalStruct):
      self._native.inner = _unwrap(value, OuterStructWithInternalAttributeStructNestedInInternalStruct)


