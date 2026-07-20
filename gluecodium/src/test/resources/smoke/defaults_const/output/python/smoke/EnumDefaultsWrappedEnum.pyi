

from smoke.EnumWrapper import EnumWrapper
import typing


from _native_base import _NativeBase

import generated


class EnumDefaultsWrappedEnum(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.EnumDefaultsWrappedEnum):
            super().__init__(args[0])
        else:
            super().__init__(generated.EnumDefaultsWrappedEnum(*[getattr(arg, "_native", arg) for arg in args]))


    @property
    def struct_field(self) -> EnumWrapper:
        """"""
        return EnumWrapper(self._native.struct_field)
    @struct_field.setter
    def struct_field(self, value: EnumWrapper):
      self._native.struct_field = getattr(value, "_native", value)


