

from enum import Enum
import typing
from typing import Optional

class DefaultValues:

    @staticmethod
    def process_struct_with_defaults(input: DefaultValues.StructWithDefaults) -> DefaultValues.StructWithDefaults:
        ...

    class StructWithDefaults:
        @typing.overload
        def __init__(self) -> None: ...
        @typing.overload
        def __init__(self, int_field: int, uint_field: int, float_field: float, double_field: float, bool_field: bool, string_field: str) -> None: ...

        int_field: int

        uint_field: int

        float_field: float

        double_field: float

        bool_field: bool

        string_field: str



    class NullableStructWithDefaults:
        @typing.overload
        def __init__(self) -> None: ...
        @typing.overload
        def __init__(self, int_field: Optional[int], uint_field: Optional[int], float_field: Optional[float], bool_field: Optional[bool], string_field: Optional[str]) -> None: ...

        int_field: Optional[int]

        uint_field: Optional[int]

        float_field: Optional[float]

        bool_field: Optional[bool]

        string_field: Optional[str]



    class StructWithSpecialDefaults:
        @typing.overload
        def __init__(self) -> None: ...
        @typing.overload
        def __init__(self, float_nan_field: float, float_infinity_field: float, float_negative_infinity_field: float, double_nan_field: float, double_infinity_field: float, double_negative_infinity_field: float) -> None: ...

        float_nan_field: float

        float_infinity_field: float

        float_negative_infinity_field: float

        double_nan_field: float

        double_infinity_field: float

        double_negative_infinity_field: float



    class StructWithEmptyDefaults:
        @typing.overload
        def __init__(self) -> None: ...
        @typing.overload
        def __init__(self, ints_field: list[int], floats_field: list[float], map_field: dict[int, str], struct_field: DefaultValues.StructWithDefaults, set_type_field: set[str]) -> None: ...

        ints_field: list[int]

        floats_field: list[float]

        map_field: dict[int, str]

        struct_field: DefaultValues.StructWithDefaults

        set_type_field: set[str]



    class StructWithTypedefDefaults:
        @typing.overload
        def __init__(self) -> None: ...
        @typing.overload
        def __init__(self, long_field: int, bool_field: bool, string_field: str) -> None: ...

        long_field: int

        bool_field: bool

        string_field: str



    LongTypedef = int



    BooleanTypedef = bool



    StringTypedef = str



    FloatArray = list[float]



    IdToStringMap = dict[int, str]



    StringSet = set[str]
