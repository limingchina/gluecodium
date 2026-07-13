

from kotlin_smoke.Currency import Currency
from kotlin_smoke.Month import Month
from kotlin_smoke.Season import Season
from kotlin_smoke.SystemColor import SystemColor
from kotlin_smoke.TimeZone import TimeZone


from _native_base import _NativeBase

import generated


class KotlinExternalTypesStruct(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], KotlinExternalTypesStruct):
            super().__init__(args[0])
        else:
            super().__init__(generated.KotlinExternalTypesStruct(*args))


    @property
    def currency(self) -> Currency:
        """"""
        return self._native.currency

    @currency.setter
    def currency(self, value: Currency):
        self._native.currency = value



    @property
    def time_zone(self) -> TimeZone:
        """"""
        return self._native.time_zone

    @time_zone.setter
    def time_zone(self, value: TimeZone):
        self._native.time_zone = value



    @property
    def month(self) -> Month:
        """"""
        return self._native.month

    @month.setter
    def month(self, value: Month):
        self._native.month = value



    @property
    def color(self) -> SystemColor:
        """"""
        return self._native.color

    @color.setter
    def color(self, value: SystemColor):
        self._native.color = value



    @property
    def season(self) -> Season:
        """"""
        return self._native.season

    @season.setter
    def season(self, value: Season):
        self._native.season = value


