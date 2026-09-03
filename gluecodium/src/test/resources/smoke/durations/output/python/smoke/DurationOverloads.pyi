

import datetime
from enum import Enum
import typing

class DurationOverloads:

    @typing.overload
    def duration_function(self, input: datetime.timedelta) -> str:
        ...

    @typing.overload
    def duration_function(self, input: str) -> str:
        ...


