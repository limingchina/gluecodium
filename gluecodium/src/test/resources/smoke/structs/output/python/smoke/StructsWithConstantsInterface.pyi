

from smoke.RouteUtils import RouteUtils
from enum import Enum
import typing
from typing import Optional

class StructsWithConstantsInterface:

    class MultiRoute:
        @typing.overload
        def __init__(self) -> None: ...
        @typing.overload
        def __init__(self, descriptions: list[str], type: RouteUtils.RouteType) -> None: ...

        descriptions: list[str]

        type: RouteUtils.RouteType


        DEFAULT_DESCRIPTION = "Foo"

        DEFAULT_TYPE = RouteUtils.RouteType.NONE


    class StructWithConstantsOnly:
        def __init__(self) -> None: ...


        DEFAULT_DESCRIPTION = "Foo"
