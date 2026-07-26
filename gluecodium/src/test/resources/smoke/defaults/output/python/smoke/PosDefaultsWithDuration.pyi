

import datetime
import typing


from _native_base import _NativeBase

import generated


class PosDefaultsWithDuration(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.smoke_PosDefaultsWithDuration):
            super().__init__(args[0])
        else:
            super().__init__(generated.smoke_PosDefaultsWithDuration(*[_unwrap(arg) for arg in args]))


    @property
    def duration_field(self) -> datetime.timedelta:
        """"""
        return _wrap(self._native.duration_field, datetime.timedelta)
    @duration_field.setter
    def duration_field(self, value: datetime.timedelta):
      self._native.duration_field = _unwrap(value, datetime.timedelta)



    @property
    def nanos_field(self) -> datetime.timedelta:
        """"""
        return _wrap(self._native.nanos_field, datetime.timedelta)
    @nanos_field.setter
    def nanos_field(self, value: datetime.timedelta):
      self._native.nanos_field = _unwrap(value, datetime.timedelta)


