

from kotlin_smoke.Currency import Currency
from kotlin_smoke.KotlinExternalTypesStruct import KotlinExternalTypesStruct
from kotlin_smoke.Month import Month
from kotlin_smoke.Season import Season
from kotlin_smoke.SystemColor import SystemColor
from kotlin_smoke.TimeZone import TimeZone
from kotlin_smoke.VeryBoolean import VeryBoolean

from _native_base import _NativeBase


class UseKotlinExternalTypes(_NativeBase):
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


    def struct_round_trip(self, input: KotlinExternalTypesStruct) -> KotlinExternalTypesStruct:
        """"""
        return self._native.struct_round_trip(input)


    def very_boolean_unbox(self, input: VeryBoolean) -> bool:
        """"""
        return self._native.very_boolean_unbox(input)

