

from smoke.Currency import Currency
from smoke.Month import Month
from smoke.Season import Season
from smoke.SystemColor import SystemColor
from smoke.TimeZone import TimeZone

class JavaExternalTypesStruct:
    """"""

    def __init__(self, native):
        self._native = native


    currency: Currency


    time_zone: TimeZone


    month: Month


    color: SystemColor


    season: Season

