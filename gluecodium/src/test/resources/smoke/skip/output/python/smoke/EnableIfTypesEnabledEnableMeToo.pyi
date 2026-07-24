

from smoke.EnableIfTypesEnabledEnableMe import EnableIfTypesEnabledEnableMe
import typing


from _native_base import _NativeBase

import generated


class EnableIfTypesEnabledEnableMeToo(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.EnableIfTypesEnabledEnableMeToo):
            super().__init__(args[0])
        else:
            super().__init__(generated.EnableIfTypesEnabledEnableMeToo(*[_unwrap(arg) for arg in args]))


    @property
    def field(self) -> EnableIfTypesEnabledEnableMe:
        """"""
        return _wrap(self._native.field, EnableIfTypesEnabledEnableMe)
    @field.setter
    def field(self, value: EnableIfTypesEnabledEnableMe):
      self._native.field = _unwrap(value, EnableIfTypesEnabledEnableMe)


