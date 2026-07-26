

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional

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
        native_result = generated.kotlin_smoke_UseKotlinExternalTypes.currency_round_trip(_unwrap(input, Currency))
        return Currency(native_result)

    @staticmethod
    def time_zone_round_trip(input: TimeZone) -> TimeZone:
        """"""
        native_result = generated.kotlin_smoke_UseKotlinExternalTypes.time_zone_round_trip(_unwrap(input, TimeZone))
        return TimeZone(native_result)

    @staticmethod
    def month_round_trip(input: Month) -> Month:
        """"""
        native_result = generated.kotlin_smoke_UseKotlinExternalTypes.month_round_trip(_unwrap(input, Month))
        return Month(native_result)

    @staticmethod
    def color_round_trip(input: SystemColor) -> SystemColor:
        """"""
        native_result = generated.kotlin_smoke_UseKotlinExternalTypes.color_round_trip(_unwrap(input, SystemColor))
        return SystemColor(native_result)

    @staticmethod
    def season_round_trip(input: Season) -> Season:
        """"""
        native_result = generated.kotlin_smoke_UseKotlinExternalTypes.season_round_trip(_unwrap(input, Season))
        return Season(native_result)

    @staticmethod
    def struct_round_trip(input: KotlinExternalTypesStruct) -> KotlinExternalTypesStruct:
        """"""
        native_result = generated.kotlin_smoke_UseKotlinExternalTypes.struct_round_trip(_unwrap(input, KotlinExternalTypesStruct))
        return KotlinExternalTypesStruct(native_result)

    @staticmethod
    def very_boolean_unbox(input: VeryBoolean) -> bool:
        """"""
        return generated.kotlin_smoke_UseKotlinExternalTypes.very_boolean_unbox(_unwrap(input, VeryBoolean))

