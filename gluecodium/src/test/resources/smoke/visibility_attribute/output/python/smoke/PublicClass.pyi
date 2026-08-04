

from enum import Enum
import typing

class PublicClass:

    def _internal_method(self, input: PublicClass._InternalStruct) -> PublicClass._InternalStruct:
        ...

    @property
    def __internal_struct_property(self) -> PublicClass._InternalStruct:
        ...

    @__internal_struct_property.setter
    def __internal_struct_property(self, value: PublicClass._InternalStruct) -> None:
        ...

    class _InternalStruct:
    
        string_field: str
    
    
    
    class PublicStruct:
    
        _internal_field: PublicClass._InternalStruct
    
    
    
    class PublicStructWithInternalDefaults:
    
        _internal_field: str
    
        public_field: float
    
    
    
    class _InternalEnum(Enum):
    
        FOO = 0
        BAR = 1
    
    
    
    _InternalArray = list[_InternalStruct]
    
    
    
    _InternalStructTypeDef = _InternalStruct
    
    
    
    _StringToInternalStructMap = dict[str, _InternalStruct]
    
    

