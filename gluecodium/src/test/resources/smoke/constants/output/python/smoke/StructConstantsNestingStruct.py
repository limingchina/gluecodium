

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional

from smoke.StructConstantsSomeStruct import StructConstantsSomeStruct


from _native_base import _NativeBase

import generated


class StructConstantsNestingStruct(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.StructConstantsNestingStruct):
            super().__init__(args[0])
        else:
            super().__init__(generated.StructConstantsNestingStruct(*[_unwrap(arg) for arg in args]))


    @property
    def struct_field(self) -> StructConstantsSomeStruct:
        """"""
        return _wrap(self._native.struct_field, StructConstantsSomeStruct)
    @struct_field.setter
    def struct_field(self, value: StructConstantsSomeStruct):
      self._native.struct_field = _unwrap(value, StructConstantsSomeStruct)


