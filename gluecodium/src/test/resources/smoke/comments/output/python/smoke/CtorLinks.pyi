

from enum import Enum
import typing

class CtorLinks:

    class SingleCtor:
        """This class has just one constructor [create]."""
    
        @staticmethod
        def create() -> CtorLinks.SingleCtor:
            ...
    
    
    
    class SingleCtorWithOneArgument:
        """This class has just one constructor with one argument [create(Int)]."""
    
        @staticmethod
        def create(arg: int) -> CtorLinks.SingleCtorWithOneArgument:
            ...
    
    
    
    class SingleCtorWithTwoArgument:
        """This class has just one constructor with two argument [create(Int, String)]."""
    
        @staticmethod
        def create(arg: int, arg2: str) -> CtorLinks.SingleCtorWithTwoArgument:
            ...
    
    
    
    class OverloadedCtors:
    
        @staticmethod
        def create(input: str) -> CtorLinks.OverloadedCtors:
            ...
    
        @staticmethod
        def create(input: str, flag: bool) -> CtorLinks.OverloadedCtors:
            """"""
            ...
    
    

