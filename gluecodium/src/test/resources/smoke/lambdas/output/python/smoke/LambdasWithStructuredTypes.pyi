

from smoke.LambdasDeclarationOrder import LambdasDeclarationOrder
from smoke.LambdasInterface import LambdasInterface
from enum import Enum
import typing
from typing import Callable

class LambdasWithStructuredTypes:

    def do_class_stuff(self, callback: Callable[[LambdasInterface], None]):
        ...

    def do_struct_stuff(self, callback: Callable[[LambdasDeclarationOrder.SomeStruct], None]):
        ...

    ClassCallback = Callable[[LambdasInterface], None]
    
    
    
    StructCallback = Callable[[LambdasDeclarationOrder.SomeStruct], None]
    
    

