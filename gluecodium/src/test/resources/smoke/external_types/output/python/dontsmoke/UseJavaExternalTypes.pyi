

from smoke.Currency import Currency
from smoke.JavaExternalTypesStruct import JavaExternalTypesStruct
from smoke.Month import Month
from smoke.Season import Season
from smoke.SystemColor import SystemColor
from smoke.TimeZone import TimeZone

from _native_base import _NativeBase


class UseJavaExternalTypes(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    def currency_round_trip(self, input: Currency) -> Currency:
        """"""
        return self._native.currency_round_trip(input)


    def time_zone_round_trip(self, input: TimeZone) -> TimeZone:
        """"""
        return self._native.time_zone_round_trip(input)


    def month_round_trip(self, input: Month) -> Month:
        """"""
        return self._native.month_round_trip(input)


    def color_round_trip(self, input: SystemColor) -> SystemColor:
        """"""
        return self._native.color_round_trip(input)


    def season_round_trip(self, input: Season) -> Season:
        """"""
        return self._native.season_round_trip(input)


    def struct_round_trip(self, input: JavaExternalTypesStruct) -> JavaExternalTypesStruct:
        """"""
        return self._native.struct_round_trip(input)

