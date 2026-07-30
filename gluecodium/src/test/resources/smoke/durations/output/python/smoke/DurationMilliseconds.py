

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper
from typing import Optional

import datetime

from _native_base import _NativeBase

import generated


class DurationMilliseconds(_NativeBase):
    def __init__(self, native):
        super().__init__(native)

    def duration_function(self, input: datetime.timedelta) -> datetime.timedelta:
        return _wrap(self._native.duration_function(_unwrap(input, datetime.timedelta)), datetime.timedelta)

    def nullable_duration_function(self, input: Optional[datetime.timedelta]) -> Optional[datetime.timedelta]:
        return _wrap(self._native.nullable_duration_function(_unwrap(input, Optional[datetime.timedelta])), Optional[datetime.timedelta])

    @property
    def duration_property(self) -> datetime.timedelta:
        return _wrap(self._native.duration_property, datetime.timedelta)

    @duration_property.setter
    def duration_property(self, value: datetime.timedelta):
        self._native.duration_property = _unwrap(value, datetime.timedelta)

