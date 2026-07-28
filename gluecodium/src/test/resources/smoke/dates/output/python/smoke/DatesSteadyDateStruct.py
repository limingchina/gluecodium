

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper
from typing import Optional

import datetime


from _native_base import _NativeBase

import generated


class DatesSteadyDateStruct(_NativeBase):
    """"""

    def __init__(self, *args, **kwargs):
        if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_DatesSteadyDateStruct):
            super().__init__(args[0])
        else:
            super().__init__(generated.smoke_DatesSteadyDateStruct(
                *[_unwrap(arg) for arg in args],
                **{k: _unwrap(v) for k, v in kwargs.items()}
            ))


    @property
    def date_field(self) -> datetime.datetime:
        """"""
        return _wrap(self._native.date_field, datetime.datetime)
    @date_field.setter
    def date_field(self, value: datetime.datetime):
      self._native.date_field = _unwrap(value, datetime.datetime)



    @property
    def nullable_date_field(self):
        """"""
        return _wrap(self._native.nullable_date_field, Optional[datetime.datetime])
    @nullable_date_field.setter
    def nullable_date_field(self, value):
      self._native.nullable_date_field = _unwrap(value, Optional[datetime.datetime])


