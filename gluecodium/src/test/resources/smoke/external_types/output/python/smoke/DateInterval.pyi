

import datetime
from enum import Enum
import typing
from typing import Optional

class DateInterval:
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, start: datetime.datetime, end: datetime.datetime) -> None: ...

    start: datetime.datetime

    end: datetime.datetime
