

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper
from typing import Optional

import datetime

from _native_base import _NativeBase

import generated


class Dates(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    def date_method(self, input: datetime.datetime) -> datetime.datetime:
        """"""
        return _wrap(self._native.date_method(_unwrap(input, datetime.datetime)), datetime.datetime)

    def nullable_date_method(self, input: Optional[datetime.datetime]) -> Optional[datetime.datetime]:
        """"""
        return _wrap(self._native.nullable_date_method(_unwrap(input, Optional[datetime.datetime])), Optional[datetime.datetime])

    @property
    def date_property(self) -> datetime.datetime:
        """"""
        return _wrap(self._native.date_property, datetime.datetime)

    @date_property.setter
    def date_property(self, value: datetime.datetime):
        self._native.date_property = _unwrap(value, datetime.datetime)

    @property
    def date_set(self) -> set[datetime.datetime]:
        """"""
        return _wrap(self._native.date_set, set[datetime.datetime])

    @date_set.setter
    def date_set(self, value: set[datetime.datetime]):
        self._native.date_set = _unwrap(value, set[datetime.datetime])

