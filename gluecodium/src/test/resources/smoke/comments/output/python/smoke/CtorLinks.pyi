

from enum import Enum
import typing

class CtorLinks:

    class SingleCtor:
        """This class has just one constructor `CtorLinks.SingleCtor`."""
    
        @staticmethod
        def create() -> CtorLinks.SingleCtor:
            ...
    
    
    
    class SingleCtorWithOneArgument:
        """This class has just one constructor with one argument `CtorLinks.SingleCtorWithOneArgument`."""
    
        @staticmethod
        def create(arg: int) -> CtorLinks.SingleCtorWithOneArgument:
            ...
    
    
    
    class SingleCtorWithTwoArgument:
        """This class has just one constructor with two argument `CtorLinks.SingleCtorWithTwoArgument`."""
    
        @staticmethod
        def create(arg: int, arg2: str) -> CtorLinks.SingleCtorWithTwoArgument:
            ...
    
    
    
    class OverloadedCtors:
    
        @typing.overload
        @staticmethod
        def create(input: str) -> CtorLinks.OverloadedCtors:
            ...
    
        @typing.overload
        @staticmethod
        def create(input: str, flag: bool) -> CtorLinks.OverloadedCtors:
            """"""
            ...
    
    

