

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



    class Line:
        @typing.overload
        def __init__(self) -> None: ...
        @typing.overload
        def __init__(self, a: TypeCollection.Point, b: TypeCollection.Point) -> None: ...

        a: TypeCollection.Point

        b: TypeCollection.Point



    class AllTypesStruct:
        @typing.overload
        def __init__(self) -> None: ...
        @typing.overload
        def __init__(self, int8_field: int, uint8_field: int, int16_field: int, uint16_field: int, int32_field: int, uint32_field: int, int64_field: int, uint64_field: int, float_field: float, double_field: float, string_field: str, boolean_field: bool, bytes_field: bytes, point_field: TypeCollection.Point) -> None: ...

        int8_field: int

        uint8_field: int

        int16_field: int

        uint16_field: int

        int32_field: int

        uint32_field: int

        int64_field: int

        uint64_field: int

        float_field: float

        double_field: float

        string_field: str

        boolean_field: bool

        bytes_field: bytes

        point_field: TypeCollection.Point



    PointTypedef = Point
