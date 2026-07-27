

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional

import datetime


from _native_base import _NativeBase

import generated


class DurationMillisecondsDurationStruct(_NativeBase):
    """"""

    def __init__(self, *args, **kwargs):
        if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_DurationMillisecondsDurationStruct):
            super().__init__(args[0])
        else:
            super().__init__(generated.smoke_DurationMillisecondsDurationStruct(
                *[_unwrap(arg) for arg in args],
                **{k: _unwrap(v) for k, v in kwargs.items()}
            ))


    @property
    def duration_field(self) -> datetime.timedelta:
        """"""
        return _wrap(self._native.duration_field, datetime.timedelta)
    @duration_field.setter
    def duration_field(self, value: datetime.timedelta):
      self._native.duration_field = _unwrap(value, datetime.timedelta)


