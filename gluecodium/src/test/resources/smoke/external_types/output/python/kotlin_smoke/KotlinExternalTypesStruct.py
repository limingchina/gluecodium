

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper
from typing import Optional

from kotlin_smoke.Currency import Currency
from kotlin_smoke.Month import Month
from kotlin_smoke.Season import Season
from kotlin_smoke.SystemColor import SystemColor
from kotlin_smoke.TimeZone import TimeZone


from _native_base import _NativeBase

import generated


class KotlinExternalTypesStruct(_NativeBase):
    """"""

    def __init__(self, *args, **kwargs):
        if len(args) == 1 and not kwargs and isinstance(args[0], generated.kotlin_smoke_KotlinExternalTypesStruct):
            super().__init__(args[0])
        else:
            super().__init__(generated.kotlin_smoke_KotlinExternalTypesStruct(
                *[_unwrap(arg) for arg in args],
                **{k: _unwrap(v) for k, v in kwargs.items()}
            ))


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


