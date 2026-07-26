

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional

from smoke.PublicClassInternalStruct import PublicClassInternalStruct


from _native_base import _NativeBase

import generated


class PublicInterfaceInternalStruct(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.smoke_PublicInterfaceInternalStruct):
            super().__init__(args[0])
        else:
            super().__init__(generated.smoke_PublicInterfaceInternalStruct(*[_unwrap(arg) for arg in args]))


    @property
    def field_of_internal_type(self) -> PublicClassInternalStruct:
        """"""
        return _wrap(self._native.field_of_internal_type, PublicClassInternalStruct)
    @field_of_internal_type.setter
    def field_of_internal_type(self, value: PublicClassInternalStruct):
      self._native.field_of_internal_type = _unwrap(value, PublicClassInternalStruct)


