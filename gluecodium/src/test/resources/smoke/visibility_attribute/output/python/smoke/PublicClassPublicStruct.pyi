

from smoke.PublicClassInternalStruct import PublicClassInternalStruct
import typing


from _native_base import _NativeBase

import generated


class PublicClassPublicStruct(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.smoke_PublicClassPublicStruct):
            super().__init__(args[0])
        else:
            super().__init__(generated.smoke_PublicClassPublicStruct(*[_unwrap(arg) for arg in args]))


    @property
    def internal_field(self) -> PublicClassInternalStruct:
        """"""
        return _wrap(self._native.internal_field, PublicClassInternalStruct)
    @internal_field.setter
    def internal_field(self, value: PublicClassInternalStruct):
      self._native.internal_field = _unwrap(value, PublicClassInternalStruct)


