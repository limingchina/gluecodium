

from __future__ import annotations

import datetime


from _native_base import _NativeBase

import generated


class DurationSecondsDurationStruct(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.DurationSecondsDurationStruct):
            super().__init__(args[0])
        else:
            super().__init__(generated.DurationSecondsDurationStruct(*[getattr(arg, "_native", arg) for arg in args]))


    @property
    def duration_field(self) -> datetime.timedelta:
        """"""
        return self._native.duration_field
    @duration_field.setter
    def duration_field(self, value: datetime.timedelta):
      self._native.duration_field = getattr(value, "_native", value)


