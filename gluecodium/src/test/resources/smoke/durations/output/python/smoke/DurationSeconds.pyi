

import datetime
import typing

from _native_base import _NativeBase

import generated


class DurationSeconds(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    def duration_function(self, input: datetime.timedelta) -> datetime.timedelta: ...

    def nullable_duration_function(self, input: Optional[datetime.timedelta]) -> Optional[datetime.timedelta]: ...

    @property
    def duration_property(self) -> datetime.timedelta:
        """"""
        return _wrap(self._native.duration_property, datetime.timedelta)

    @duration_property.setter
    def duration_property(self, value: datetime.timedelta):
        self._native.duration_property = _unwrap(value, datetime.timedelta)

