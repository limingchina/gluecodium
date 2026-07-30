

from smoke.PropertiesExampleStruct import PropertiesExampleStruct
from smoke.PropertiesInterface import PropertiesInterface
from smoke.PropertiesInternalErrorCode import PropertiesInternalErrorCode
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
    def struct_property(self) -> PropertiesExampleStruct:
        ...

    @struct_property.setter
    def struct_property(self, value: PropertiesExampleStruct) -> None:
        ...

    @property
    def array_property(self) -> list[str]:
        ...

    @array_property.setter
    def array_property(self, value: list[str]) -> None:
        ...

    @property
    def complex_type_property(self) -> PropertiesInternalErrorCode:
        ...

    @complex_type_property.setter
    def complex_type_property(self, value: PropertiesInternalErrorCode) -> None:
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
    def static_readonly_property(self) -> PropertiesExampleStruct:
        ...


