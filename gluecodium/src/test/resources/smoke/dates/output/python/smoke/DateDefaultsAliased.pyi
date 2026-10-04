

import datetime
from enum import Enum
import typing
from typing import Optional

class DateDefaultsAliased:
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, date_time: datetime.datetime, date_time_utc: datetime.datetime, before_epoch: datetime.datetime, exactly_epoch: datetime.datetime) -> None: ...

    date_time: datetime.datetime

    date_time_utc: datetime.datetime

    before_epoch: datetime.datetime

    exactly_epoch: datetime.datetime
