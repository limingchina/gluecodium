

from kotlin_smoke.Currency import Currency
from kotlin_smoke.Month import Month
from kotlin_smoke.Season import Season
from kotlin_smoke.SystemColor import SystemColor
from kotlin_smoke.TimeZone import TimeZone

from _native_base import _NativeBase


class KotlinExternalTypesStruct(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    currency: Currency


    time_zone: TimeZone


    month: Month


    color: SystemColor


    season: Season

