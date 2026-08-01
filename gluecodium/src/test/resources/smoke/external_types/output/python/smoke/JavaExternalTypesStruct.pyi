

from smoke.Currency import Currency
from smoke.Month import Month
from smoke.Season import Season
from smoke.SystemColor import SystemColor
from smoke.TimeZone import TimeZone
from enum import Enum
import typing

class JavaExternalTypesStruct:

    currency: Currency

    time_zone: TimeZone

    month: Month

    color: SystemColor

    season: Season


