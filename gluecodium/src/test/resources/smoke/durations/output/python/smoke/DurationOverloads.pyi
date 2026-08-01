

import datetime
from enum import Enum
import typing

class DurationOverloads:

    def duration_function(self, input: datetime.timedelta) -> str:
        ...

    def duration_function(self, input: str) -> str:
        ...


