

from enum import Enum
import typing

class InnerClassForwardDeclarations:

    class InnerClass1:
    
    
    
    class InnerClass2:
    
        class InnerInnerClass1:
    
            def foo(self) -> InnerClassForwardDeclarations.InnerClass2.InnerInnerClass2:
                ...
    
    
    
        class InnerInnerClass2:
    
            def bar(self, arg: InnerClassForwardDeclarations.InnerInterface2):
                ...
    
    
    
    
    class InnerInterface2:
    
    
    
    class InnerInterface3:
    
    

