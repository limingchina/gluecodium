

import datetime
from enum import Enum
import typing
from typing import Optional

class DurationDefaults:
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, dayz: datetime.timedelta, hourz: datetime.timedelta, minutez: datetime.timedelta, secondz: datetime.timedelta, milliz: datetime.timedelta, microz: datetime.timedelta, nanoz: datetime.timedelta) -> None: ...

    dayz: datetime.timedelta

    hourz: datetime.timedelta

    minutez: datetime.timedelta

    secondz: datetime.timedelta

    milliz: datetime.timedelta

    microz: datetime.timedelta

    nanoz: datetime.timedelta
