

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional

from smoke.FcStruct import FcStruct


from _native_base import _NativeBase

import generated


class DefaultsWithFcStruct(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.smoke_DefaultsWithFcStruct):
            super().__init__(args[0])
        else:
            super().__init__(generated.smoke_DefaultsWithFcStruct(*[_unwrap(arg) for arg in args]))


    @property
    def struct_field(self) -> FcStruct:
        """"""
        return _wrap(self._native.struct_field, FcStruct)
    @struct_field.setter
    def struct_field(self, value: FcStruct):
      self._native.struct_field = _unwrap(value, FcStruct)


