

from enum import Enum
import typing
from typing import Optional

class TypesWithDefaults:
    def __init__(self) -> None: ...

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



    class ImmutableStructWithDefaults:
        @typing.overload
        def __init__(self, uint_field: int, bool_field: bool) -> None: ...
        @typing.overload
        def __init__(self, int_field: int, uint_field: int, float_field: float, double_field: float, bool_field: bool, string_field: str) -> None: ...

        int_field: int

        uint_field: int

        float_field: float

        double_field: float

        bool_field: bool

        string_field: str



    class ImmutableStructWithCollections:
        @typing.overload
        def __init__(self) -> None: ...
        @typing.overload
        def __init__(self, nullable_list_field: Optional[list[int]], empty_list_field: list[int], values_list_field: list[int], nullable_map_field: Optional[dict[int, str]], empty_map_field: dict[int, str], values_map_field: dict[int, str], nullable_set_field: Optional[set[str]], empty_set_field: set[str], values_set_field: set[str]) -> None: ...

        nullable_list_field: Optional[list[int]]

        empty_list_field: list[int]

        values_list_field: list[int]

        nullable_map_field: Optional[dict[int, str]]

        empty_map_field: dict[int, str]

        values_map_field: dict[int, str]

        nullable_set_field: Optional[set[str]]

        empty_set_field: set[str]

        values_set_field: set[str]



    class ImmutableStructWithFieldConstructorAndCollections:
        @typing.overload
        def __init__(self) -> None: ...
        @typing.overload
        def __init__(self, nullable_list_field: Optional[list[int]], empty_list_field: list[int], values_list_field: list[int], nullable_map_field: Optional[dict[int, str]], empty_map_field: dict[int, str], values_map_field: dict[int, str], nullable_set_field: Optional[set[str]], empty_set_field: set[str], values_set_field: set[str], some_field: int, another_field: int) -> None: ...
        @typing.overload
        def __init__(self, some_field: int, another_field: int) -> None: ...

        nullable_list_field: Optional[list[int]]

        empty_list_field: list[int]

        values_list_field: list[int]

        nullable_map_field: Optional[dict[int, str]]

        empty_map_field: dict[int, str]

        values_map_field: dict[int, str]

        nullable_set_field: Optional[set[str]]

        empty_set_field: set[str]

        values_set_field: set[str]

        some_field: int

        another_field: int



    class SomeImmutableStructWithDefaults:
        @typing.overload
        def __init__(self) -> None: ...
        @typing.overload
        def __init__(self, int_field: int) -> None: ...

        int_field: int



    class ImmutableStructWithFieldUsingImmutableStruct:
        @typing.overload
        def __init__(self) -> None: ...
        @typing.overload
        def __init__(self, some_field1: TypesWithDefaults.SomeImmutableStructWithDefaults, some_field2: TypesWithDefaults.ImmutableStructWithCollections) -> None: ...

        some_field1: TypesWithDefaults.SomeImmutableStructWithDefaults

        some_field2: TypesWithDefaults.ImmutableStructWithCollections



    class ImmutableStructWithFieldConstructorAndFieldUsingImmutableStruct:
        @typing.overload
        def __init__(self) -> None: ...
        @typing.overload
        def __init__(self, some_field1: TypesWithDefaults.SomeImmutableStructWithDefaults, some_field2: TypesWithDefaults.ImmutableStructWithCollections, some_field: int, another_field: int) -> None: ...
        @typing.overload
        def __init__(self, some_field: int, another_field: int) -> None: ...

        some_field1: TypesWithDefaults.SomeImmutableStructWithDefaults

        some_field2: TypesWithDefaults.ImmutableStructWithCollections

        some_field: int

        another_field: int



    class ImmutableStructWithNullableFieldUsingImmutableStruct:
        @typing.overload
        def __init__(self) -> None: ...
        @typing.overload
        def __init__(self, some_field1: Optional[TypesWithDefaults.SomeImmutableStructWithDefaults], some_field2: Optional[TypesWithDefaults.ImmutableStructWithCollections]) -> None: ...

        some_field1: Optional[TypesWithDefaults.SomeImmutableStructWithDefaults]

        some_field2: Optional[TypesWithDefaults.ImmutableStructWithCollections]



    class ImmutableStructWithFieldConstructorAndNullableFieldUsingImmutableStruct:
        @typing.overload
        def __init__(self) -> None: ...
        @typing.overload
        def __init__(self, some_field1: Optional[TypesWithDefaults.SomeImmutableStructWithDefaults], some_field2: Optional[TypesWithDefaults.ImmutableStructWithCollections], some_field: int, another_field: int) -> None: ...
        @typing.overload
        def __init__(self, some_field: int, another_field: int) -> None: ...

        some_field1: Optional[TypesWithDefaults.SomeImmutableStructWithDefaults]

        some_field2: Optional[TypesWithDefaults.ImmutableStructWithCollections]

        some_field: int

        another_field: int
