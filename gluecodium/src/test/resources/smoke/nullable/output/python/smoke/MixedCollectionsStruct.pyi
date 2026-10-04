

import datetime
from enum import Enum
import typing
from typing import Optional

class MixedCollectionsStruct:

    almost_dates: list[Optional[datetime.datetime]]

    dates: list[datetime.datetime]
