

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional

from smoke.OrderInStructNestedStruct import OrderInStructNestedStruct
from smoke.OrderInStructSomeEnum import OrderInStructSomeEnum


from _native_base import _NativeBase

import generated


class OrderInStruct(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.OrderInStruct):
            super().__init__(args[0])
        else:
            super().__init__(generated.OrderInStruct(*[_unwrap(arg) for arg in args]))


    @property
    def struct_field(self) -> OrderInStructNestedStruct:
        """"""
        return _wrap(self._native.struct_field, OrderInStructNestedStruct)
    @struct_field.setter
    def struct_field(self, value: OrderInStructNestedStruct):
      self._native.struct_field = _unwrap(value, OrderInStructNestedStruct)



    @property
    def enum_field(self) -> OrderInStructSomeEnum:
        """"""
        return _wrap(self._native.enum_field, OrderInStructSomeEnum)
    @enum_field.setter
    def enum_field(self, value: OrderInStructSomeEnum):
      self._native.enum_field = _unwrap(value, OrderInStructSomeEnum)


