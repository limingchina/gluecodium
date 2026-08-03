

from enum import Enum
import typing
from typing import Callable

class ExcludedComments:
    """This is some very useful class."""

    def some_method_with_all_comments(self, input_parameter: str) -> bool:
        """This is some very useful method that measures the usefulness of its input."""
        ...

    def some_method_without_return_type_or_input_parameters(self):
        """This is some very useful method that does nothing."""
        ...

    @property
    def is_some_property(self) -> bool:
        """Some very useful property."""
        ...

    @is_some_property.setter
    def is_some_property(self, value: bool) -> None:
        """Sets some very useful property."""
        ...

    class SomeStruct:
        """This is some very useful struct."""
    
        #: How useful this struct is
        #: remains to be seen
        some_field: bool
    
    
    
    class SomeEnum(Enum):
        """This is some very useful enum."""
    
        USELESS = 0
    
    
    
    class SomethingWrongError(Exception):
        """This is some very useful exception."""
        message: str
    
        def __init__(self, message: str) -> None: ...
    
    
    
    #: This is some very useful typealias.
    Usefulness = bool
    
    
    
    #: This is some very useful lambda that does it.
    SomeLambda = Callable[[str, int], float]
    
    

    #: This is some very useful constant.
    VERY_USEFUL = True

