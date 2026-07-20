

from smoke.ImmutableStructNoClash import ImmutableStructNoClash
import typing


from _native_base import _NativeBase

import generated


class MutableStructImmutableFields(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.MutableStructImmutableFields):
            super().__init__(args[0])
        else:
            super().__init__(generated.MutableStructImmutableFields(*[getattr(arg, "_native", arg) for arg in args]))


    @property
    def struct_field(self) -> ImmutableStructNoClash:
        """"""
        return ImmutableStructNoClash(self._native.struct_field)



    @property
    def int_field(self) -> int:
        """"""
        return self._native.int_field
    @int_field.setter
    def int_field(self, value: int):
      self._native.int_field = getattr(value, "_native", value)



    @property
    def bool_field(self) -> bool:
        """"""
        return self._native.bool_field
    @bool_field.setter
    def bool_field(self, value: bool):
      self._native.bool_field = getattr(value, "_native", value)


