

from smoke.NonEquatableClass import NonEquatableClass
from smoke.NonEquatableInterface import NonEquatableInterface
from enum import Enum
import typing
from typing import Optional

class SimpleEquatableStruct:
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, class_field: NonEquatableClass, interface_field: NonEquatableInterface) -> None: ...
    @typing.overload
    def __init__(self, class_field: NonEquatableClass, interface_field: NonEquatableInterface, nullable_class_field: Optional[NonEquatableClass], nullable_interface_field: Optional[NonEquatableInterface]) -> None: ...
    def __eq__(self, other: object) -> bool: ...
    __hash__ = None  # type: ignore[assignment]
    def as_key(self) -> _gluecodium_key_736d6f6b652e53696d706c65457175617461626c65537472756374: ...

    class_field: NonEquatableClass

    interface_field: NonEquatableInterface

    nullable_class_field: Optional[NonEquatableClass]

    nullable_interface_field: Optional[NonEquatableInterface]



class _gluecodium_key_736d6f6b652e53696d706c65457175617461626c65537472756374(SimpleEquatableStruct):
    def __hash__(self) -> int: ...  # type: ignore[override]
