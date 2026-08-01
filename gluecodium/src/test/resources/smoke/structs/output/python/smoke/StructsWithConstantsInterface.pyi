

from smoke.RouteUtils import RouteUtils
from enum import Enum
import typing

class StructsWithConstantsInterface:

    class MultiRoute:
    
        descriptions: list[str]
    
        type: RouteUtils.RouteType
    
        DEFAULT_DESCRIPTION = "Foo"
    
        DEFAULT_TYPE = RouteType.NONE
    
    
    
    class StructWithConstantsOnly:
    
        DEFAULT_DESCRIPTION = "Foo"
    
    

