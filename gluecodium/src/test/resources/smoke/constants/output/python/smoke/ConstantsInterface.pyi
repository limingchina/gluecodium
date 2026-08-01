

from enum import Enum
import typing

class ConstantsInterface:

    BOOL_CONSTANT = True

    INT_CONSTANT = -11

    UINT_CONSTANT = 4294967295

    FLOAT_CONSTANT = 2.71

    DOUBLE_CONSTANT = -3.14

    STRING_CONSTANT = "Foo bar"

    ENUM_CONSTANT = StateEnum.ON

    class StateEnum(Enum):
    
        OFF = 0
        ON = 1
    
    

