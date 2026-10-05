

from enum import Enum
import typing
from typing import Optional

class TypeCollection:
    def __init__(self) -> None: ...

    class Point:
        @typing.overload
        def __init__(self) -> None: ...
        @typing.overload
        def __init__(self, x: float, y: float) -> None: ...

        x: float

        y: float



    class StructHavingAliasFieldDefinedBelow:
        @typing.overload
        def __init__(self) -> None: ...
        @typing.overload
        def __init__(self, field: int) -> None: ...

        field: int



    PointTypeDef = Point



    StorageId = int



    INVALID_STORAGE_ID = 0
