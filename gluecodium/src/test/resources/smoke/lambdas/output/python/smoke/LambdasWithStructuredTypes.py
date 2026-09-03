

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase
from enum import Enum
from typing import Optional
from typing import Callable
import generated

from smoke.LambdasDeclarationOrder import LambdasDeclarationOrder
from smoke.LambdasInterface import LambdasInterface

class LambdasWithStructuredTypes(_NativeBase):
    def __init__(self, native):
        super().__init__(native)

    def do_class_stuff(self, callback: Callable[[LambdasInterface], None]):
        return _wrap(self._native.do_class_stuff(_unwrap(callback, Callable[[LambdasInterface], None])), None)

    def do_struct_stuff(self, callback: Callable[[LambdasDeclarationOrder.SomeStruct], None]):
        return _wrap(self._native.do_struct_stuff(_unwrap(callback, Callable[[LambdasDeclarationOrder.SomeStruct], None])), None)

    ClassCallback = Callable[[LambdasInterface], None]
    
    
    
    StructCallback = Callable[[LambdasDeclarationOrder.SomeStruct], None]
    
    

