

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional

from smoke.OrderInStructWithFunctionsNestedStruct import OrderInStructWithFunctionsNestedStruct
from smoke.OrderInStructWithFunctionsSomeEnum import OrderInStructWithFunctionsSomeEnum


from _native_base import _NativeBase

import generated


class OrderInStructWithFunctions(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.OrderInStructWithFunctions):
            super().__init__(args[0])
        else:
            super().__init__(generated.OrderInStructWithFunctions(*[_unwrap(arg) for arg in args]))


    @property
    def some_field(self) -> str:
        """"""
        return _wrap(self._native.some_field, str)
    @some_field.setter
    def some_field(self, value: str):
      self._native.some_field = _unwrap(value, str)


    def do_stuff(self, struct_foo: OrderInStructWithFunctionsNestedStruct) -> OrderInStructWithFunctionsSomeEnum:
        """"""
        return _wrap(self._native.do_stuff(_unwrap(struct_foo, OrderInStructWithFunctionsNestedStruct)), OrderInStructWithFunctionsSomeEnum)

