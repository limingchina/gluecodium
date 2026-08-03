

from fire.Enum1 import Enum1
from fire.Enum2 import Enum2
from fire.Enum3 import Enum3
from fire.Enum4 import Enum4
from smoke.EnumWrapper import EnumWrapper
from enum import Enum
import typing

class EnumDefaults:

    class SimpleEnum:
    
        enum_field: Enum1
    
    
    
    class NullableEnum:
    
        enum_field1: Optional[Enum2]
    
        enum_field1: Optional[Enum2]
    
    
    
    class AliasEnum:
    
        enum_field: Enum3
    
    
    
    class WrappedEnum:
    
        struct_field: EnumWrapper
    
    
    
    EnumAlias = Enum3
    
    

