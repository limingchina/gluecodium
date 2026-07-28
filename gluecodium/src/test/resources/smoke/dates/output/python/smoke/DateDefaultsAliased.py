

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper
from typing import Optional

import datetime


from _native_base import _NativeBase

import generated


class DateDefaultsAliased(_NativeBase):
    """"""

    def __init__(self, *args, **kwargs):
        if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_DateDefaultsAliased):
            super().__init__(args[0])
        else:
            super().__init__(generated.smoke_DateDefaultsAliased(
                *[_unwrap(arg) for arg in args],
                **{k: _unwrap(v) for k, v in kwargs.items()}
            ))


    @property
    def date_time(self) -> datetime.datetime:
        """"""
        return _wrap(self._native.date_time, datetime.datetime)
    @date_time.setter
    def date_time(self, value: datetime.datetime):
      self._native.date_time = _unwrap(value, datetime.datetime)



    @property
    def date_time_utc(self) -> datetime.datetime:
        """"""
        return _wrap(self._native.date_time_utc, datetime.datetime)
    @date_time_utc.setter
    def date_time_utc(self, value: datetime.datetime):
      self._native.date_time_utc = _unwrap(value, datetime.datetime)



    @property
    def before_epoch(self) -> datetime.datetime:
        """"""
        return _wrap(self._native.before_epoch, datetime.datetime)
    @before_epoch.setter
    def before_epoch(self, value: datetime.datetime):
      self._native.before_epoch = _unwrap(value, datetime.datetime)



    @property
    def exactly_epoch(self) -> datetime.datetime:
        """"""
        return _wrap(self._native.exactly_epoch, datetime.datetime)
    @exactly_epoch.setter
    def exactly_epoch(self, value: datetime.datetime):
      self._native.exactly_epoch = _unwrap(value, datetime.datetime)


