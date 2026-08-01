

from enum import Enum
import typing

class PropertiesInterface:

    @property
    def struct_property(self) -> PropertiesInterface.ExampleStruct:
        ...

    @struct_property.setter
    def struct_property(self, value: PropertiesInterface.ExampleStruct) -> None:
        ...

    class ExampleStruct:
    
        value: float
    
    

