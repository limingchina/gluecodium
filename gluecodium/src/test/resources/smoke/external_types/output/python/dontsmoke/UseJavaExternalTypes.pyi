

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
        native_result = generated.UseJavaExternalTypes.currency_round_trip(input)
        return Currency(native_result)

    @staticmethod

    def time_zone_round_trip(input: TimeZone) -> TimeZone:
        """"""
        native_result = generated.UseJavaExternalTypes.time_zone_round_trip(input)
        return TimeZone(native_result)

    @staticmethod

    def month_round_trip(input: Month) -> Month:
        """"""
        native_result = generated.UseJavaExternalTypes.month_round_trip(input)
        return Month(native_result)

    @staticmethod

    def color_round_trip(input: SystemColor) -> SystemColor:
        """"""
        native_result = generated.UseJavaExternalTypes.color_round_trip(input)
        return SystemColor(native_result)

    @staticmethod

    def season_round_trip(input: Season) -> Season:
        """"""
        native_result = generated.UseJavaExternalTypes.season_round_trip(input)
        return Season(native_result)

    @staticmethod

    def struct_round_trip(input: JavaExternalTypesStruct) -> JavaExternalTypesStruct:
        """"""
        native_result = generated.UseJavaExternalTypes.struct_round_trip(input)
        return JavaExternalTypesStruct(native_result)

