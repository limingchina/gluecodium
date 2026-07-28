

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper
from typing import Optional

import datetime

from _native_base import _NativeBase

import generated


class DatesSteady(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    def date_method(self, input: datetime.datetime) -> datetime.datetime:
        """"""
        return _wrap(self._native.date_method(_unwrap(input, datetime.datetime)), datetime.datetime)

    def nullable_date_method(self, input: Optional[datetime.datetime]) -> Optional[datetime.datetime]:
        """"""
        return _wrap(self._native.nullable_date_method(_unwrap(input, Optional[datetime.datetime])), Optional[datetime.datetime])

    def date_list_method(self, input: list[datetime.datetime]) -> list[datetime.datetime]:
        """"""
        return _wrap(self._native.date_list_method(_unwrap(input, list[datetime.datetime])), list[datetime.datetime])

