

import datetime
from enum import Enum
import typing
from typing import Optional

class PosDefaultsWithDuration:
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, duration_field: datetime.timedelta, nanos_field: datetime.timedelta) -> None: ...

    duration_field: datetime.timedelta

    nanos_field: datetime.timedelta
