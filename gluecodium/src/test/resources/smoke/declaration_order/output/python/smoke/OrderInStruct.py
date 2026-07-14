

from __future__ import annotations

from smoke.OrderInStructNestedStruct import OrderInStructNestedStruct
from smoke.SomeEnum import SomeEnum


from _native_base import _NativeBase

import generated


class OrderInStruct(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], OrderInStruct):
            super().__init__(args[0])
        else:
            super().__init__(generated.OrderInStruct(*[getattr(arg, "_native", arg) for arg in args]))


    @property
    def struct_field(self) -> OrderInStructNestedStruct:
        """"""
        return OrderInStructNestedStruct(self._native.struct_field)

    @struct_field.setter
    def struct_field(self, value: OrderInStructNestedStruct):
      self._native.struct_field = getattr(value, "_native", value)



    @property
    def enum_field(self) -> SomeEnum:
        """"""
        return SomeEnum(self._native.enum_field)

    @enum_field.setter
    def enum_field(self, value: SomeEnum):
      self._native.enum_field = getattr(value, "_native", value)

from enum import Enum


class SomeEnum(Enum):
    """"""

    FOO = 0
    BAR = 1


