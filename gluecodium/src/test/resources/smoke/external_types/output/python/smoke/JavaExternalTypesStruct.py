

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional

from smoke.Currency import Currency
from smoke.Month import Month
from smoke.Season import Season
from smoke.SystemColor import SystemColor
from smoke.TimeZone import TimeZone


from _native_base import _NativeBase

import generated


class JavaExternalTypesStruct(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.JavaExternalTypesStruct):
            super().__init__(args[0])
        else:
            super().__init__(generated.JavaExternalTypesStruct(*[_unwrap(arg) for arg in args]))


    @property
    def currency(self) -> Currency:
        """"""
        return _wrap(self._native.currency, Currency)



    @property
    def time_zone(self) -> TimeZone:
        """"""
        return _wrap(self._native.time_zone, TimeZone)
    @time_zone.setter
    def time_zone(self, value: TimeZone):
      self._native.time_zone = _unwrap(value, TimeZone)



    @property
    def month(self) -> Month:
        """"""
        return _wrap(self._native.month, Month)
    @month.setter
    def month(self, value: Month):
      self._native.month = _unwrap(value, Month)



    @property
    def color(self) -> SystemColor:
        """"""
        return _wrap(self._native.color, SystemColor)
    @color.setter
    def color(self, value: SystemColor):
      self._native.color = _unwrap(value, SystemColor)



    @property
    def season(self) -> Season:
        """"""
        return _wrap(self._native.season, Season)
    @season.setter
    def season(self, value: Season):
      self._native.season = _unwrap(value, Season)


