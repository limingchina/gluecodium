

from enum import Enum
import typing

class CppRefReturnType:

    @staticmethod
    def void_ref():
        ...

    @staticmethod
    def bool_ref() -> bool:
        ...

    @staticmethod
    def string_ref() -> str:
        ...

    @staticmethod
    def struct_ref() -> CppRefReturnType.SomeStruct:
        ...

    @staticmethod
    def class_ref() -> CppRefReturnType:
        ...

    @staticmethod
    def nullable_ref() -> Optional[str]:
        ...

    @staticmethod
    def throwing_enum_with_void():
        ...

    @staticmethod
    def throwing_enum_with_string() -> str:
        ...

    @staticmethod
    def throwing_struct_with_void():
        ...

    @staticmethod
    def throwing_struct_with_string() -> str:
        ...

    @property
    def string_property(self) -> str:
        ...


    class SomeStruct:
    
        field: str
    
    
    
    class InternalError(Enum):
    
        FOO = 0
        BAR = 1
    
    
    
    class EnumBasedError(Exception):
        message: str
    
        def __init__(self, message: str) -> None: ...
    
    
    
    class StructBasedError(Exception):
        message: str
    
        def __init__(self, message: str) -> None: ...
    
    

