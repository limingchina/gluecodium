

from __future__ import annotations



from _native_base import _NativeBase

import generated


class OuterStructWithInternalAttributeStructNestedInInternalStruct(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.OuterStructWithInternalAttributeStructNestedInInternalStruct):
            super().__init__(args[0])
        else:
            super().__init__(generated.OuterStructWithInternalAttributeStructNestedInInternalStruct(*[getattr(arg, "_native", arg) for arg in args]))


    @property
    def some_field(self) -> int:
        """"""
        return self._native.some_field
    @some_field.setter
    def some_field(self, value: int):
      self._native.some_field = getattr(value, "_native", value)


