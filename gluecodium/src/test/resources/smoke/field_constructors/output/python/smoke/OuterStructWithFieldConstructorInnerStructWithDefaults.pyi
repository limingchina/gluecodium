

import typing


from _native_base import _NativeBase

import generated


class OuterStructWithFieldConstructorInnerStructWithDefaults(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.OuterStructWithFieldConstructorInnerStructWithDefaults):
            super().__init__(args[0])
        else:
            super().__init__(generated.OuterStructWithFieldConstructorInnerStructWithDefaults(*[getattr(arg, "_native", arg) for arg in args]))


    @property
    def inner_struct_field(self) -> float:
        """"""
        return self._native.inner_struct_field
    @inner_struct_field.setter
    def inner_struct_field(self, value: float):
      self._native.inner_struct_field = getattr(value, "_native", value)


