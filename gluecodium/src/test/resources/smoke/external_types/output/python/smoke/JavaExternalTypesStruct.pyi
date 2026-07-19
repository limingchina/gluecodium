

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
            super().__init__(generated.JavaExternalTypesStruct(*[getattr(arg, "_native", arg) for arg in args]))


    @property
    def currency(self) -> Currency:
        """"""
        return Currency(self._native.currency)



    @property
    def time_zone(self) -> TimeZone:
        """"""
        return TimeZone(self._native.time_zone)
    @time_zone.setter
    def time_zone(self, value: TimeZone):
      self._native.time_zone = getattr(value, "_native", value)



    @property
    def month(self) -> Month:
        """"""
        return Month(self._native.month)
    @month.setter
    def month(self, value: Month):
      self._native.month = getattr(value, "_native", value)



    @property
    def color(self) -> SystemColor:
        """"""
        return SystemColor(self._native.color)
    @color.setter
    def color(self, value: SystemColor):
      self._native.color = getattr(value, "_native", value)



    @property
    def season(self) -> Season:
        """"""
        return Season(self._native.season)
    @season.setter
    def season(self, value: Season):
      self._native.season = getattr(value, "_native", value)


