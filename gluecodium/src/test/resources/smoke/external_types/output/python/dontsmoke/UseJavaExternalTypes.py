

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper
from typing import Optional

from smoke.Currency import Currency
from smoke.JavaExternalTypesStruct import JavaExternalTypesStruct
from smoke.Month import Month
from smoke.Season import Season
from smoke.SystemColor import SystemColor
from smoke.TimeZone import TimeZone

from _native_base import _NativeBase

import generated


class UseJavaExternalTypes(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    @staticmethod
    def currency_round_trip(input: Currency) -> Currency:
        """"""
        native_result = generated.dontsmoke_UseJavaExternalTypes.currency_round_trip(_unwrap(input, Currency))
        return _get_or_create_wrapper(native_result, Currency)

    @staticmethod
    def time_zone_round_trip(input: TimeZone) -> TimeZone:
        """"""
        native_result = generated.dontsmoke_UseJavaExternalTypes.time_zone_round_trip(_unwrap(input, TimeZone))
        return _get_or_create_wrapper(native_result, TimeZone)

    @staticmethod
    def month_round_trip(input: Month) -> Month:
        """"""
        native_result = generated.dontsmoke_UseJavaExternalTypes.month_round_trip(_unwrap(input, Month))
        return _get_or_create_wrapper(native_result, Month)

    @staticmethod
    def color_round_trip(input: SystemColor) -> SystemColor:
        """"""
        native_result = generated.dontsmoke_UseJavaExternalTypes.color_round_trip(_unwrap(input, SystemColor))
        return _get_or_create_wrapper(native_result, SystemColor)

    @staticmethod
    def season_round_trip(input: Season) -> Season:
        """"""
        native_result = generated.dontsmoke_UseJavaExternalTypes.season_round_trip(_unwrap(input, Season))
        return _get_or_create_wrapper(native_result, Season)

    @staticmethod
    def struct_round_trip(input: JavaExternalTypesStruct) -> JavaExternalTypesStruct:
        """"""
        native_result = generated.dontsmoke_UseJavaExternalTypes.struct_round_trip(_unwrap(input, JavaExternalTypesStruct))
        return _get_or_create_wrapper(native_result, JavaExternalTypesStruct)

