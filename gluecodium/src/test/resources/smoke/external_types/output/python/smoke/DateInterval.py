

from __future__ import annotations

import datetime


from _native_base import _NativeBase

import generated


class DateInterval(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], DateInterval):
            super().__init__(args[0])
        else:
            super().__init__(generated.DateInterval(*[getattr(arg, "_native", arg) for arg in args]))


    @property
    def start(self) -> datetime.datetime:
        """"""
        return self._native.start

    @start.setter
    def start(self, value: datetime.datetime):
      self._native.start = getattr(value, "_native", value)



    @property
    def end(self) -> datetime.datetime:
        """"""
        return self._native.end

    @end.setter
    def end(self, value: datetime.datetime):
      self._native.end = getattr(value, "_native", value)


