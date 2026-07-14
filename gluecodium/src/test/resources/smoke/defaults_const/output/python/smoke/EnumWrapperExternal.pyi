

from fire.ExternalEnum4 import ExternalEnum4


from _native_base import _NativeBase

import generated


class EnumWrapperExternal(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], EnumWrapperExternal):
            super().__init__(args[0])
        else:
            super().__init__(generated.EnumWrapperExternal(*[getattr(arg, "_native", arg) for arg in args]))


    @property
    def enum_field(self) -> ExternalEnum4:
        """"""
        return ExternalEnum4(self._native.enum_field)

    @enum_field.setter
    def enum_field(self, value: ExternalEnum4):
      self._native.enum_field = getattr(value, "_native", value)


