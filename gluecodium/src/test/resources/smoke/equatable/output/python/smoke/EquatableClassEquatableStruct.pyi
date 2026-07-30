

from smoke.PointerEquatableClass import PointerEquatableClass
import typing

class EquatableClassEquatableStruct:
    def __eq__(self, other: object) -> bool: ...
    def __hash__(self) -> int: ...

    int_field: int

    string_field: str

    nested_equatable_instance: EquatableClass

    nested_pointer_equatable_instance: PointerEquatableClass

