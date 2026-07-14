

from __future__ import annotations

from smoke.SomethingEnum import SomethingEnum


from _native_base import _NativeBase

import generated


class StructWithPosEnums(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], StructWithPosEnums):
            super().__init__(args[0])
        else:
            super().__init__(generated.StructWithPosEnums(*[getattr(arg, "_native", arg) for arg in args]))


    @property
    def first_field(self) -> SomethingEnum:
        """"""
        return SomethingEnum(self._native.first_field)

    @first_field.setter
    def first_field(self, value: SomethingEnum):
      self._native.first_field = getattr(value, "_native", value)



    @property
    def explicit_field(self) -> SomethingEnum:
        """"""
        return SomethingEnum(self._native.explicit_field)

    @explicit_field.setter
    def explicit_field(self, value: SomethingEnum):
      self._native.explicit_field = getattr(value, "_native", value)



    @property
    def last_field(self) -> SomethingEnum:
        """"""
        return SomethingEnum(self._native.last_field)

    @last_field.setter
    def last_field(self, value: SomethingEnum):
      self._native.last_field = getattr(value, "_native", value)



FIRST_CONSTANT = SomethingEnum.REALLY_FIRST

