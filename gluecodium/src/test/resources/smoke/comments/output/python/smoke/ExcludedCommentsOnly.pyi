

from enum import Enum
import typing
from typing import Callable

class ExcludedCommentsOnly:
    """"""

    def some_method_with_all_comments(self, input_parameter: str) -> bool:
        """"""
        ...

    def some_method_without_return_type_or_input_parameters(self):
        """"""
        ...

    @property
    def is_some_property(self) -> bool:
        """"""
        ...

    @is_some_property.setter
    def is_some_property(self, value: bool) -> None:
        ...

    class SomeStruct:
        """"""
    
        #: 
        some_field: bool
    
    
    
    class SomeEnum(Enum):
        """"""
    
        USELESS = 0
    
    
    
    class SomethingWrongError(Exception):
        """"""
        message: str
    
        def __init__(self, message: str) -> None: ...
    
    
    
    #: 
    Usefulness = bool
    
    
    
    #: 
    SomeLambda = Callable[[str, int], float]
    
    

    #: 
    VERY_USEFUL = True

