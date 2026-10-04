

import datetime
from enum import Enum
import typing
from typing import Optional

class DurationInterface:

    def duration_function(self, input: datetime.timedelta) -> str:
        ...
