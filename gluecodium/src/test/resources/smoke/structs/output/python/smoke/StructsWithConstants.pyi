

from smoke.RouteUtils import RouteUtils
from enum import Enum
import typing
from typing import Optional

class StructsWithConstants:
    def __init__(self) -> None: ...

    class Route:
        @typing.overload
        def __init__(self) -> None: ...
        @typing.overload
        def __init__(self, description: str, type: RouteUtils.RouteType) -> None: ...

        description: str

        type: RouteUtils.RouteType


        DEFAULT_DESCRIPTION = "Nonsense"

        DEFAULT_TYPE = RouteUtils.RouteType.EQUESTRIAN
