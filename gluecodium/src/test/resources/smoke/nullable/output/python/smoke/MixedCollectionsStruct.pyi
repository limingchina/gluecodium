

import datetime
from enum import Enum
import typing
from typing import Optional

class MixedCollectionsStruct:
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, almost_dates: list[Optional[datetime.datetime]], dates: list[datetime.datetime]) -> None: ...

    almost_dates: list[Optional[datetime.datetime]]

    dates: list[datetime.datetime]
