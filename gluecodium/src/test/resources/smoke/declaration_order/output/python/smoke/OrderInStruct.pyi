

from smoke.OrderInStructNestedStruct import OrderInStructNestedStruct
from smoke.OrderInStructSomeEnum import OrderInStructSomeEnum
import typing


from _native_base import _NativeBase

import generated


class OrderInStruct(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.OrderInStruct):
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
    def enum_field(self) -> OrderInStructSomeEnum:
        """"""
        return OrderInStructSomeEnum(self._native.enum_field)
    @enum_field.setter
    def enum_field(self, value: OrderInStructSomeEnum):
      self._native.enum_field = getattr(value, "_native", value)


