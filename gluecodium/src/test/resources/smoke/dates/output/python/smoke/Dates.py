

from __future__ import annotations

import datetime


from _native_base import _NativeBase

import generated


class Dates(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    def date_method(self, input: datetime.datetime) -> datetime.datetime:
        """"""
        return self._native.date_method(input)


    def nullable_date_method(self, input: Optional[datetime.datetime]) -> Optional[datetime.datetime]:
        """"""
        return self._native.nullable_date_method(input)


    @property
    def date_property(self) -> datetime.datetime:
        """"""
        return self._native.date_property

    @date_property.setter
    def date_property(self, value: datetime.datetime):
        self._native.date_property = value


    @property
    def date_set(self) -> set[datetime.datetime]:
        """"""
        return self._native.date_set

    @date_set.setter
    def date_set(self, value: set[datetime.datetime]):
        self._native.date_set = value

