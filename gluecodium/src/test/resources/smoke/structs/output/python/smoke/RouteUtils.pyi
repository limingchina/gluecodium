

from enum import Enum
import typing
from typing import Optional

class RouteUtils:

    class RouteType(Enum):

        NONE = 0
        CAR = 1
        PEDESTRIAN = 2
        EQUESTRIAN = 3
