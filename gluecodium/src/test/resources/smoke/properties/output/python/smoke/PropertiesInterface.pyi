

from enum import Enum
import typing
from typing import Optional

class PropertiesInterface:

    @property
    def struct_property(self) -> PropertiesInterface.ExampleStruct:
        ...

    @struct_property.setter
    def struct_property(self, value: PropertiesInterface.ExampleStruct) -> None:
        ...

    class ExampleStruct:
        @typing.overload
        def __init__(self) -> None: ...
        @typing.overload
        def __init__(self, value: float) -> None: ...

        value: float
