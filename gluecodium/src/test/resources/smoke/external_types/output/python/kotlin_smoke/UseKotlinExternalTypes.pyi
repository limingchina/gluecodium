

from kotlin_smoke.Currency import Currency
from kotlin_smoke.KotlinExternalTypesStruct import KotlinExternalTypesStruct
from kotlin_smoke.Month import Month
from kotlin_smoke.Season import Season
from kotlin_smoke.SystemColor import SystemColor
from kotlin_smoke.TimeZone import TimeZone
from kotlin_smoke.VeryBoolean import VeryBoolean
import typing

class UseKotlinExternalTypes:

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
    def struct_round_trip(input: KotlinExternalTypesStruct) -> KotlinExternalTypesStruct:
        ...

    @staticmethod
    def very_boolean_unbox(input: VeryBoolean) -> bool:
        ...

