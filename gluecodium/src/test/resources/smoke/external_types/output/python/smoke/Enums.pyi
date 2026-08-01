

from enum import Enum
import typing

class Enums:

    @staticmethod
    def method_with_external_enum(input: Enums.ExternalEnum):
        ...

    class ExternalEnum(Enum):
    
        FOO_VALUE = 0
        BAR_VALUE = 1
    
    
    
    class VeryExternalEnum(Enum):
    
        FOO = 0
        BAR = 1
    
    

