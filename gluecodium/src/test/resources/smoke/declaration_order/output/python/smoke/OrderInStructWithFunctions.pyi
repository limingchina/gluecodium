

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
            super().__init__(generated.OrderInStructWithFunctions(*[getattr(arg, "_native", arg) for arg in args]))


    @property
    def some_field(self) -> str:
        """"""
        return self._native.some_field
    @some_field.setter
    def some_field(self, value: str):
      self._native.some_field = getattr(value, "_native", value)


    def do_stuff(self, struct_foo: OrderInStructWithFunctionsNestedStruct) -> OrderInStructWithFunctionsSomeEnum:
        """"""
        return self._native.do_stuff(struct_foo._native)

