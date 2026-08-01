

from enum import Enum
import typing

class EnableIfTypesEnabled:

    PLACE_HOLDER_ENABLED = True

    class EnableMeToo:
    
        field: EnableIfTypesEnabled.EnableMe
    
    
    
    class EnableMe(Enum):
    
        NOPE = 0
    
    

