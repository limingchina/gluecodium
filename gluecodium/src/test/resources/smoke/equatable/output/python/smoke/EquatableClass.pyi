

from smoke.PointerEquatableClass import PointerEquatableClass
from enum import Enum
import typing
from typing import Optional

class EquatableClass:

    class EquatableStruct:
        @typing.overload
        def __init__(self) -> None: ...
        @typing.overload
        def __init__(self, int_field: int, string_field: str, nested_equatable_instance: EquatableClass, nested_pointer_equatable_instance: PointerEquatableClass) -> None: ...
        def __eq__(self, other: object) -> bool: ...
        __hash__ = None  # type: ignore[assignment]
        def as_key(self) -> _gluecodium_key_736d6f6b652e457175617461626c65436c6173732e457175617461626c65537472756374: ...

        int_field: int

        string_field: str

        nested_equatable_instance: EquatableClass

        nested_pointer_equatable_instance: PointerEquatableClass




class _gluecodium_key_736d6f6b652e457175617461626c65436c6173732e457175617461626c65537472756374(EquatableClass.EquatableStruct):
    def __hash__(self) -> int: ...  # type: ignore[override]
