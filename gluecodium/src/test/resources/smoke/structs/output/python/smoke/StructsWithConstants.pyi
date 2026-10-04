

from smoke.RouteUtils import RouteUtils
from enum import Enum
import typing
from typing import Optional

class StructsWithConstants:

    class Route:

        description: str

        type: RouteUtils.RouteType


        DEFAULT_DESCRIPTION = "Nonsense"

        DEFAULT_TYPE = RouteUtils.RouteType.EQUESTRIAN
