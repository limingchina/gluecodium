

import datetime
from enum import Enum
import typing

class DurationInterface:

    def duration_function(self, input: datetime.timedelta) -> str:
        ...


