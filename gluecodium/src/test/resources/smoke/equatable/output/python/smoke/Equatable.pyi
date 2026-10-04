

from enum import Enum
import typing
from typing import Optional

class Equatable:

    class EquatableStruct:
        def __eq__(self, other: object) -> bool: ...
        __hash__ = None  # type: ignore[assignment]
        def as_key(self) -> _gluecodium_key_736d6f6b652e457175617461626c652e457175617461626c65537472756374: ...

        bool_field: bool

        int_field: int

        long_field: int

        float_field: float

        double_field: float

        string_field: str

        struct_field: Equatable.NestedEquatableStruct

        enum_field: Equatable.SomeEnum

        array_field: list[str]

        map_field: dict[int, str]



    class EquatableNullableStruct:
        def __eq__(self, other: object) -> bool: ...
        __hash__ = None  # type: ignore[assignment]
        def as_key(self) -> _gluecodium_key_736d6f6b652e457175617461626c652e457175617461626c654e756c6c61626c65537472756374: ...

        bool_field: Optional[bool]

        int_field: Optional[int]

        uint_field: Optional[int]

        float_field: Optional[float]

        string_field: Optional[str]

        struct_field: Optional[Equatable.NestedEquatableStruct]

        enum_field: Optional[Equatable.SomeEnum]

        array_field: Optional[list[str]]

        map_field: Optional[dict[int, str]]



    class NestedEquatableStruct:
        def __eq__(self, other: object) -> bool: ...
        __hash__ = None  # type: ignore[assignment]
        def as_key(self) -> _gluecodium_key_736d6f6b652e457175617461626c652e4e6573746564457175617461626c65537472756374: ...

        foo_field: str



    class SomeEnum(Enum):

        FOO = 0
        BAR = 1



    ErrorCodeToMessageMap = dict[int, str]




class _gluecodium_key_736d6f6b652e457175617461626c652e457175617461626c65537472756374(Equatable.EquatableStruct):
    def __hash__(self) -> int: ...  # type: ignore[override]
class _gluecodium_key_736d6f6b652e457175617461626c652e457175617461626c654e756c6c61626c65537472756374(Equatable.EquatableNullableStruct):
    def __hash__(self) -> int: ...  # type: ignore[override]
class _gluecodium_key_736d6f6b652e457175617461626c652e4e6573746564457175617461626c65537472756374(Equatable.NestedEquatableStruct):
    def __hash__(self) -> int: ...  # type: ignore[override]
