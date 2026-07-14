

from __future__ import annotations

import datetime


from _native_base import _NativeBase

import generated


class DateDefaultsAliased(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], DateDefaultsAliased):
            super().__init__(args[0])
        else:
            super().__init__(generated.DateDefaultsAliased(*[getattr(arg, "_native", arg) for arg in args]))


    @property
    def date_time(self) -> datetime.datetime:
        """"""
        return self._native.date_time

    @date_time.setter
    def date_time(self, value: datetime.datetime):
      self._native.date_time = getattr(value, "_native", value)



    @property
    def date_time_utc(self) -> datetime.datetime:
        """"""
        return self._native.date_time_utc

    @date_time_utc.setter
    def date_time_utc(self, value: datetime.datetime):
      self._native.date_time_utc = getattr(value, "_native", value)



    @property
    def before_epoch(self) -> datetime.datetime:
        """"""
        return self._native.before_epoch

    @before_epoch.setter
    def before_epoch(self, value: datetime.datetime):
      self._native.before_epoch = getattr(value, "_native", value)



    @property
    def exactly_epoch(self) -> datetime.datetime:
        """"""
        return self._native.exactly_epoch

    @exactly_epoch.setter
    def exactly_epoch(self, value: datetime.datetime):
      self._native.exactly_epoch = getattr(value, "_native", value)


