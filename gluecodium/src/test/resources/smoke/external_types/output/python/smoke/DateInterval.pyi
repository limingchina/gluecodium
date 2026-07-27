

import datetime
import typing


from _native_base import _NativeBase

import generated


class DateInterval(_NativeBase):
    """"""

    def __init__(self, *args, **kwargs):
        if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_DateInterval):
            super().__init__(args[0])
        else:
            super().__init__(generated.smoke_DateInterval(
                *[_unwrap(arg) for arg in args],
                **{k: _unwrap(v) for k, v in kwargs.items()}
            ))


    @property
    def start(self) -> datetime.datetime:
        """"""
        return _wrap(self._native.start, datetime.datetime)
    @start.setter
    def start(self, value: datetime.datetime):
      self._native.start = _unwrap(value, datetime.datetime)



    @property
    def end(self) -> datetime.datetime:
        """"""
        return _wrap(self._native.end, datetime.datetime)
    @end.setter
    def end(self, value: datetime.datetime):
      self._native.end = _unwrap(value, datetime.datetime)


