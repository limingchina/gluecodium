

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase
from enum import Enum
from typing import Optional
import generated

from kotlin_smoke.Currency import Currency
from kotlin_smoke.KotlinExternalTypesStruct import KotlinExternalTypesStruct
from kotlin_smoke.Month import Month
from kotlin_smoke.Season import Season
from kotlin_smoke.SystemColor import SystemColor
from kotlin_smoke.TimeZone import TimeZone
from kotlin_smoke.VeryBoolean import VeryBoolean

class UseKotlinExternalTypes(_NativeBase):
    def __init__(self, native):
        super().__init__(native)

    @staticmethod
    def currency_round_trip(input: Currency) -> Currency:
        native_result = generated.kotlin_smoke_UseKotlinExternalTypes.currency_round_trip(_unwrap(input, Currency))
        return _get_or_create_wrapper(native_result, Currency)

    @staticmethod
    def time_zone_round_trip(input: TimeZone) -> TimeZone:
        native_result = generated.kotlin_smoke_UseKotlinExternalTypes.time_zone_round_trip(_unwrap(input, TimeZone))
        return _get_or_create_wrapper(native_result, TimeZone)

    @staticmethod
    def month_round_trip(input: Month) -> Month:
        native_result = generated.kotlin_smoke_UseKotlinExternalTypes.month_round_trip(_unwrap(input, Month))
        return _get_or_create_wrapper(native_result, Month)

    @staticmethod
    def color_round_trip(input: SystemColor) -> SystemColor:
        native_result = generated.kotlin_smoke_UseKotlinExternalTypes.color_round_trip(_unwrap(input, SystemColor))
        return _get_or_create_wrapper(native_result, SystemColor)

    @staticmethod
    def season_round_trip(input: Season) -> Season:
        native_result = generated.kotlin_smoke_UseKotlinExternalTypes.season_round_trip(_unwrap(input, Season))
        return _get_or_create_wrapper(native_result, Season)

    @staticmethod
    def struct_round_trip(input: KotlinExternalTypesStruct) -> KotlinExternalTypesStruct:
        native_result = generated.kotlin_smoke_UseKotlinExternalTypes.struct_round_trip(_unwrap(input, KotlinExternalTypesStruct))
        return _get_or_create_wrapper(native_result, KotlinExternalTypesStruct)

    @staticmethod
    def very_boolean_unbox(input: VeryBoolean) -> bool:
        return generated.kotlin_smoke_UseKotlinExternalTypes.very_boolean_unbox(_unwrap(input, VeryBoolean))


