

from __future__ import annotations

import datetime


from _native_base import _NativeBase

import generated


class PosDefaultsWithDuration(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.PosDefaultsWithDuration):
            super().__init__(args[0])
        else:
            super().__init__(generated.PosDefaultsWithDuration(*[getattr(arg, "_native", arg) for arg in args]))


    @property
    def duration_field(self) -> datetime.timedelta:
        """"""
        return self._native.duration_field
    @duration_field.setter
    def duration_field(self, value: datetime.timedelta):
      self._native.duration_field = getattr(value, "_native", value)



    @property
    def nanos_field(self) -> datetime.timedelta:
        """"""
        return self._native.nanos_field
    @nanos_field.setter
    def nanos_field(self, value: datetime.timedelta):
      self._native.nanos_field = getattr(value, "_native", value)


