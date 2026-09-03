

from smoke.PropertiesInterface import PropertiesInterface
from enum import Enum
import typing

class Properties:

    @property
    def built_in_type_property(self) -> int:
        ...

    @built_in_type_property.setter
    def built_in_type_property(self, value: int) -> None:
        ...

    @property
    def readonly_property(self) -> float:
        ...


    @property
    def struct_property(self) -> Properties.ExampleStruct:
        ...

    @struct_property.setter
    def struct_property(self, value: Properties.ExampleStruct) -> None:
        ...

    @property
    def array_property(self) -> list[str]:
        ...

    @array_property.setter
    def array_property(self, value: list[str]) -> None:
        ...

    @property
    def complex_type_property(self) -> Properties.InternalErrorCode:
        ...

    @complex_type_property.setter
    def complex_type_property(self, value: Properties.InternalErrorCode) -> None:
        ...

    @property
    def byte_buffer_property(self) -> bytes:
        ...

    @byte_buffer_property.setter
    def byte_buffer_property(self, value: bytes) -> None:
        ...

    @property
    def instance_property(self) -> PropertiesInterface:
        ...

    @instance_property.setter
    def instance_property(self, value: PropertiesInterface) -> None:
        ...

    @property
    def is_boolean_property(self) -> bool:
        ...

    @is_boolean_property.setter
    def is_boolean_property(self, value: bool) -> None:
        ...

    @property
    def static_property(self) -> str:
        ...

    @static_property.setter
    def static_property(self, value: str) -> None:
        ...

    @property
    def static_readonly_property(self) -> Properties.ExampleStruct:
        ...


    class ExampleStruct:
    
        value: float
    
    
    
    class InternalErrorCode(Enum):
    
        ERROR_NONE = 0
        ERROR_FATAL = 1
    
    

