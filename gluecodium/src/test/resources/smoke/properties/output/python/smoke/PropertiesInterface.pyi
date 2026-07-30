

from smoke.PropertiesInterfaceExampleStruct import PropertiesInterfaceExampleStruct
import typing

class PropertiesInterface:

    @property
    def struct_property(self) -> PropertiesInterfaceExampleStruct:
        ...

    @struct_property.setter
    def struct_property(self, value: PropertiesInterfaceExampleStruct) -> None:
        ...

