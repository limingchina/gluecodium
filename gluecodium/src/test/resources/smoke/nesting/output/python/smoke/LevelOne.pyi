

from smoke.OuterClass import OuterClass
from smoke.OuterInterface import OuterInterface
from enum import Enum
import typing

class LevelOne:

    class LevelTwo:
    
        class LevelThree:
    
            def foo(self, input: OuterClass.InnerInterface) -> OuterInterface.InnerClass:
                ...
    
            class LevelFour:
    
                string_field: str
    
                @staticmethod
                def foo_factory() -> LevelOne.LevelTwo.LevelThree.LevelFour:
                    ...
    
                FOO = False
    
    
    
            class LevelFourEnum(Enum):
    
                NONE = 0
    
    
    
    

