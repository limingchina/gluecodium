

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional

from smoke.OuterStructWithInternalAttributeStructNestedInInternalStruct import OuterStructWithInternalAttributeStructNestedInInternalStruct


from _native_base import _NativeBase

import generated


class OuterStructWithInternalAttribute(_NativeBase):
    """"""

    def __init__(self, *args, **kwargs):
        if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_OuterStructWithInternalAttribute):
            super().__init__(args[0])
        else:
            super().__init__(generated.smoke_OuterStructWithInternalAttribute(
                *[_unwrap(arg) for arg in args],
                **{k: _unwrap(v) for k, v in kwargs.items()}
            ))


    @property
    def inner(self) -> OuterStructWithInternalAttributeStructNestedInInternalStruct:
        """"""
        return _wrap(self._native.inner, OuterStructWithInternalAttributeStructNestedInInternalStruct)
    @inner.setter
    def inner(self, value: OuterStructWithInternalAttributeStructNestedInInternalStruct):
      self._native.inner = _unwrap(value, OuterStructWithInternalAttributeStructNestedInInternalStruct)


