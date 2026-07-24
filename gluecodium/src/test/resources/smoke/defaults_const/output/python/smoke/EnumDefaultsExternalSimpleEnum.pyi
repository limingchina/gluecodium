

from fire.ExternalEnum1 import ExternalEnum1
import typing


from _native_base import _NativeBase

import generated


class EnumDefaultsExternalSimpleEnum(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.EnumDefaultsExternalSimpleEnum):
            super().__init__(args[0])
        else:
            super().__init__(generated.EnumDefaultsExternalSimpleEnum(*[_unwrap(arg) for arg in args]))


    @property
    def enum_field(self) -> ExternalEnum1:
        """"""
        return _wrap(self._native.enum_field, ExternalEnum1)
    @enum_field.setter
    def enum_field(self, value: ExternalEnum1):
      self._native.enum_field = _unwrap(value, ExternalEnum1)


