

from __future__ import annotations

from smoke.FcStruct import FcStruct


from _native_base import _NativeBase

import generated


class DefaultsWithFcStruct(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.DefaultsWithFcStruct):
            super().__init__(args[0])
        else:
            super().__init__(generated.DefaultsWithFcStruct(*[getattr(arg, "_native", arg) for arg in args]))


    @property
    def struct_field(self) -> FcStruct:
        """"""
        return FcStruct(self._native.struct_field)
    @struct_field.setter
    def struct_field(self, value: FcStruct):
      self._native.struct_field = getattr(value, "_native", value)


