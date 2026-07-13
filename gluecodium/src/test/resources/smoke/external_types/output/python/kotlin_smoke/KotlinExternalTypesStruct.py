

from kotlin_smoke.Currency import Currency
from kotlin_smoke.Month import Month
from kotlin_smoke.Season import Season
from kotlin_smoke.SystemColor import SystemColor
from kotlin_smoke.TimeZone import TimeZone

class KotlinExternalTypesStruct:
    """"""

    def __init__(self, native):
        self._native = native


    currency: Currency


    time_zone: TimeZone


    month: Month


    color: SystemColor


    season: Season

