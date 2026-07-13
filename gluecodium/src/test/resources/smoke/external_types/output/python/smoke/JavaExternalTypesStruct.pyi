

from smoke.Currency import Currency
from smoke.Month import Month
from smoke.Season import Season
from smoke.SystemColor import SystemColor
from smoke.TimeZone import TimeZone

from _native_base import _NativeBase


class JavaExternalTypesStruct(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    currency: Currency


    time_zone: TimeZone


    month: Month


    color: SystemColor


    season: Season

