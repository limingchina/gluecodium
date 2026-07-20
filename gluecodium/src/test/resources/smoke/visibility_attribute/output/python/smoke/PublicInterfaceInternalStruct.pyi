

from smoke.PublicClassInternalStruct import PublicClassInternalStruct
import typing


from _native_base import _NativeBase

import generated


class PublicInterfaceInternalStruct(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.PublicInterfaceInternalStruct):
            super().__init__(args[0])
        else:
            super().__init__(generated.PublicInterfaceInternalStruct(*[getattr(arg, "_native", arg) for arg in args]))


    @property
    def field_of_internal_type(self) -> PublicClassInternalStruct:
        """"""
        return PublicClassInternalStruct(self._native.field_of_internal_type)
    @field_of_internal_type.setter
    def field_of_internal_type(self, value: PublicClassInternalStruct):
      self._native.field_of_internal_type = getattr(value, "_native", value)


