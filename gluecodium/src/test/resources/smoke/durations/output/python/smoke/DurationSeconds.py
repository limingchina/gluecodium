

from __future__ import annotations

import datetime


from _native_base import _NativeBase

import generated


class DurationSeconds(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    def duration_function(self, input: datetime.timedelta) -> datetime.timedelta:
        """"""
        return self._native.duration_function(input)


    def nullable_duration_function(self, input: Optional[datetime.timedelta]) -> Optional[datetime.timedelta]:
        """"""
        return self._native.nullable_duration_function(input)


    @property
    def duration_property(self) -> datetime.timedelta:
        """"""
        return self._native.duration_property

    @duration_property.setter
    def duration_property(self, value: datetime.timedelta):
        self._native.duration_property = value

