

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional

from smoke.OrderInClassNestedStruct import OrderInClassNestedStruct
from smoke.OrderInClassSomeEnum import OrderInClassSomeEnum


from _native_base import _NativeBase

import generated


class OrderInClassMainStruct(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.smoke_OrderInClassMainStruct):
            super().__init__(args[0])
        else:
            super().__init__(generated.smoke_OrderInClassMainStruct(*[_unwrap(arg) for arg in args]))


    @property
    def struct_field(self) -> OrderInClassNestedStruct:
        """"""
        return _wrap(self._native.struct_field, OrderInClassNestedStruct)
    @struct_field.setter
    def struct_field(self, value: OrderInClassNestedStruct):
      self._native.struct_field = _unwrap(value, OrderInClassNestedStruct)



    @property
    def type_def_field(self) -> int:
        """"""
        return _wrap(self._native.type_def_field, int)
    @type_def_field.setter
    def type_def_field(self, value: int):
      self._native.type_def_field = _unwrap(value, int)



    @property
    def struct_array_field(self) -> list[OrderInClassNestedStruct]:
        """"""
        return _wrap(self._native.struct_array_field, list[OrderInClassNestedStruct])
    @struct_array_field.setter
    def struct_array_field(self, value: list[OrderInClassNestedStruct]):
      self._native.struct_array_field = _unwrap(value, list[OrderInClassNestedStruct])



    @property
    def map_field(self) -> dict[int, list[OrderInClassNestedStruct]]:
        """"""
        return _wrap(self._native.map_field, dict[int, list[OrderInClassNestedStruct]])
    @map_field.setter
    def map_field(self, value: dict[int, list[OrderInClassNestedStruct]]):
      self._native.map_field = _unwrap(value, dict[int, list[OrderInClassNestedStruct]])



    @property
    def enum_field(self) -> OrderInClassSomeEnum:
        """"""
        return _wrap(self._native.enum_field, OrderInClassSomeEnum)
    @enum_field.setter
    def enum_field(self, value: OrderInClassSomeEnum):
      self._native.enum_field = _unwrap(value, OrderInClassSomeEnum)


