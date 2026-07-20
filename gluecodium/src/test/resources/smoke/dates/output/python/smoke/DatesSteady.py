

from __future__ import annotations

import datetime

from _native_base import _NativeBase

import generated


class DatesSteady(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    def date_method(self, input: datetime.datetime) -> datetime.datetime:
        """"""
        return self._native.date_method(input)

    def nullable_date_method(self, input: Optional[datetime.datetime]) -> Optional[datetime.datetime]:
        """"""
        return self._native.nullable_date_method(input)

    def date_list_method(self, input: list[datetime.datetime]) -> list[datetime.datetime]:
        """"""
        return self._native.date_list_method(input)

