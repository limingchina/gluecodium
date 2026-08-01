

import datetime
from smoke.FreeEnum import FreeEnum
from smoke.FreeError import FreeError
from smoke.FreePoint import FreePoint
from enum import Enum
import typing

class UseFreeTypes:

    def do_stuff(self, point: FreePoint, mode: FreeEnum) -> datetime.datetime:
        ...


