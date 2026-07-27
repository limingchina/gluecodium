

from fire.ExternalEnum4 import ExternalEnum4
import typing


from _native_base import _NativeBase

import generated


class EnumWrapperExternal(_NativeBase):
    """"""

    def __init__(self, *args, **kwargs):
        if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_EnumWrapperExternal):
            super().__init__(args[0])
        else:
            super().__init__(generated.smoke_EnumWrapperExternal(
                *[_unwrap(arg) for arg in args],
                **{k: _unwrap(v) for k, v in kwargs.items()}
            ))


    @property
    def enum_field(self) -> ExternalEnum4:
        """"""
        return _wrap(self._native.enum_field, ExternalEnum4)
    @enum_field.setter
    def enum_field(self, value: ExternalEnum4):
      self._native.enum_field = _unwrap(value, ExternalEnum4)


