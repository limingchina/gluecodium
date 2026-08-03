

from fire.ExternalEnum1 import ExternalEnum1
from fire.ExternalEnum2 import ExternalEnum2
from fire.ExternalEnum3 import ExternalEnum3
from fire.ExternalEnum4 import ExternalEnum4
from smoke.EnumWrapper import EnumWrapper
from enum import Enum
import typing

class EnumDefaultsExternal:

    class SimpleEnum:
    
        enum_field: ExternalEnum1
    
    
    
    class NullableEnum:
    
        enum_field1: Optional[ExternalEnum2]
    
        enum_field2: Optional[ExternalEnum2]
    
    
    
    class AliasEnum:
    
        enum_field: ExternalEnum3
    
    
    
    class WrappedEnum:
    
        struct_field: EnumWrapper
    
    
    
    EnumAlias = ExternalEnum3
    
    

