

import typing


from _native_base import _NativeBase

import generated


class OrderInStructNestedStruct(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.OrderInStructNestedStruct):
            super().__init__(args[0])
        else:
            super().__init__(generated.OrderInStructNestedStruct(*[getattr(arg, "_native", arg) for arg in args]))


    @property
    def some_field(self) -> str:
        """"""
        return self._native.some_field
    @some_field.setter
    def some_field(self, value: str):
      self._native.some_field = getattr(value, "_native", value)


