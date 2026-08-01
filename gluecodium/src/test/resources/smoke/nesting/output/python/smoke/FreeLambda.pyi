

import datetime
from smoke.FreeEnum import FreeEnum
from enum import Enum
import typing
from typing import Callable

FreeLambda = Callable[[datetime.datetime], FreeEnum]


