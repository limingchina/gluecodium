

from __future__ import annotations

from smoke.FcStruct import FcStruct


from _native_base import _NativeBase

import generated


class DefaultsWithFcStruct(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], DefaultsWithFcStruct):
            super().__init__(args[0])
        else:
            super().__init__(generated.DefaultsWithFcStruct(*args))


    @property
    def struct_field(self) -> FcStruct:
        """"""
        return self._native.struct_field

    @struct_field.setter
    def struct_field(self, value: FcStruct):
        self._native.struct_field = value


