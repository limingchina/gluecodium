

from smoke.Currency import Currency
from smoke.JavaExternalTypesStruct import JavaExternalTypesStruct
from smoke.Month import Month
from smoke.Season import Season
from smoke.SystemColor import SystemColor
from smoke.TimeZone import TimeZone
from enum import Enum
import typing

class UseJavaExternalTypes:

    @staticmethod
    def currency_round_trip(input: Currency) -> Currency:
        ...

    @staticmethod
    def time_zone_round_trip(input: TimeZone) -> TimeZone:
        ...

    @staticmethod
    def month_round_trip(input: Month) -> Month:
        ...

    @staticmethod
    def color_round_trip(input: SystemColor) -> SystemColor:
        ...

    @staticmethod
    def season_round_trip(input: Season) -> Season:
        ...

    @staticmethod
    def struct_round_trip(input: JavaExternalTypesStruct) -> JavaExternalTypesStruct:
        ...


