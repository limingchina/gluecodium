

from __future__ import annotations

from fire.ExternalEnum1 import ExternalEnum1


from _native_base import _NativeBase

import generated


class EnumDefaultsExternalSimpleEnum(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.EnumDefaultsExternalSimpleEnum):
            super().__init__(args[0])
        else:
            super().__init__(generated.EnumDefaultsExternalSimpleEnum(*[getattr(arg, "_native", arg) for arg in args]))


    @property
    def enum_field(self) -> ExternalEnum1:
        """"""
        return ExternalEnum1(self._native.enum_field)
    @enum_field.setter
    def enum_field(self, value: ExternalEnum1):
      self._native.enum_field = getattr(value, "_native", value)


