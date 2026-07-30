

from smoke.NonEquatableClass import NonEquatableClass
from smoke.NonEquatableInterface import NonEquatableInterface
import typing

class SimpleEquatableStruct:
    def __eq__(self, other: object) -> bool: ...
    def __hash__(self) -> int: ...

    class_field: NonEquatableClass

    interface_field: NonEquatableInterface

    nullable_class_field: Optional[NonEquatableClass]

    nullable_interface_field: Optional[NonEquatableInterface]

