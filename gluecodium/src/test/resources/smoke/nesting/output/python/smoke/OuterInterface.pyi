

from enum import Enum
import typing

class OuterInterface:

    def foo(self, input: str) -> str:
        ...

    class InnerClass:
    
        def foo(self, input: str) -> str:
            ...
    
    
    
    class InnerInterface:
    
        def foo(self, input: str) -> str:
            ...
    
    

