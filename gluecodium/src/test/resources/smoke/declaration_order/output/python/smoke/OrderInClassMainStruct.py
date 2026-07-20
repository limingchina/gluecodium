

from __future__ import annotations

from smoke.OrderInClassNestedStruct import OrderInClassNestedStruct
from smoke.OrderInClassSomeEnum import OrderInClassSomeEnum


from _native_base import _NativeBase

import generated


class OrderInClassMainStruct(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.OrderInClassMainStruct):
            super().__init__(args[0])
        else:
            super().__init__(generated.OrderInClassMainStruct(*[getattr(arg, "_native", arg) for arg in args]))


    @property
    def struct_field(self) -> OrderInClassNestedStruct:
        """"""
        return OrderInClassNestedStruct(self._native.struct_field)
    @struct_field.setter
    def struct_field(self, value: OrderInClassNestedStruct):
      self._native.struct_field = getattr(value, "_native", value)



    @property
    def type_def_field(self) -> int:
        """"""
        return self._native.type_def_field
    @type_def_field.setter
    def type_def_field(self, value: int):
      self._native.type_def_field = getattr(value, "_native", value)



    @property
    def struct_array_field(self) -> list[OrderInClassNestedStruct]:
        """"""
        return self._native.struct_array_field
    @struct_array_field.setter
    def struct_array_field(self, value: list[OrderInClassNestedStruct]):
      self._native.struct_array_field = getattr(value, "_native", value)



    @property
    def map_field(self) -> dict[int, list[OrderInClassNestedStruct]]:
        """"""
        return self._native.map_field
    @map_field.setter
    def map_field(self, value: dict[int, list[OrderInClassNestedStruct]]):
      self._native.map_field = getattr(value, "_native", value)



    @property
    def enum_field(self) -> OrderInClassSomeEnum:
        """"""
        return OrderInClassSomeEnum(self._native.enum_field)
    @enum_field.setter
    def enum_field(self, value: OrderInClassSomeEnum):
      self._native.enum_field = getattr(value, "_native", value)


