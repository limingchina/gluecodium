

from __future__ import annotations

from kotlin_smoke.Currency import Currency
from kotlin_smoke.KotlinExternalTypesStruct import KotlinExternalTypesStruct
from kotlin_smoke.Month import Month
from kotlin_smoke.Season import Season
from kotlin_smoke.SystemColor import SystemColor
from kotlin_smoke.TimeZone import TimeZone
from kotlin_smoke.VeryBoolean import VeryBoolean


from _native_base import _NativeBase

import generated


class UseKotlinExternalTypes(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    @staticmethod

    def currency_round_trip(input: Currency) -> Currency:
        """"""
        native_result = generated.UseKotlinExternalTypes.currency_round_trip(input)
        return Currency(native_result)

    @staticmethod

    def time_zone_round_trip(input: TimeZone) -> TimeZone:
        """"""
        native_result = generated.UseKotlinExternalTypes.time_zone_round_trip(input)
        return TimeZone(native_result)

    @staticmethod

    def month_round_trip(input: Month) -> Month:
        """"""
        native_result = generated.UseKotlinExternalTypes.month_round_trip(input)
        return Month(native_result)

    @staticmethod

    def color_round_trip(input: SystemColor) -> SystemColor:
        """"""
        native_result = generated.UseKotlinExternalTypes.color_round_trip(input)
        return SystemColor(native_result)

    @staticmethod

    def season_round_trip(input: Season) -> Season:
        """"""
        native_result = generated.UseKotlinExternalTypes.season_round_trip(input)
        return Season(native_result)

    @staticmethod

    def struct_round_trip(input: KotlinExternalTypesStruct) -> KotlinExternalTypesStruct:
        """"""
        native_result = generated.UseKotlinExternalTypes.struct_round_trip(input)
        return KotlinExternalTypesStruct(native_result)

    @staticmethod

    def very_boolean_unbox(input: VeryBoolean) -> bool:
        """"""
        native_result = generated.UseKotlinExternalTypes.very_boolean_unbox(input)
        return bool(native_result)

