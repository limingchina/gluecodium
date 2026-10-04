

from enum import Enum
import typing
from typing import Optional

class RouteUtils:
    def __init__(self) -> None: ...

    class RouteType(Enum):

        NONE = 0
        CAR = 1
        PEDESTRIAN = 2
        EQUESTRIAN = 3
