

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional

import datetime


from _native_base import _NativeBase

import generated


class DurationMillisecondsDurationStruct(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.DurationMillisecondsDurationStruct):
            super().__init__(args[0])
        else:
            super().__init__(generated.DurationMillisecondsDurationStruct(*[_unwrap(arg) for arg in args]))


    @property
    def duration_field(self) -> datetime.timedelta:
        """"""
        return _wrap(self._native.duration_field, datetime.timedelta)
    @duration_field.setter
    def duration_field(self, value: datetime.timedelta):
      self._native.duration_field = _unwrap(value, datetime.timedelta)


