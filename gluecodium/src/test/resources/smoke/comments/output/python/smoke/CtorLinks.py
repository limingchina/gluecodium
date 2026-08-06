

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase
from enum import Enum
from typing import Optional
import generated


class CtorLinks(_NativeBase):
    def __init__(self, native):
        super().__init__(native)

    class SingleCtor(_NativeBase):
        """This class has just one constructor `CtorLinks.SingleCtor`."""
        def __init__(self, native):
            super().__init__(native)
    
        @staticmethod
        def create() -> CtorLinks.SingleCtor:
            native_result = generated.smoke_CtorLinks.SingleCtor.create()
            return _get_or_create_wrapper(native_result, CtorLinks.SingleCtor)
    
    
    
    class SingleCtorWithOneArgument(_NativeBase):
        """This class has just one constructor with one argument `CtorLinks.SingleCtorWithOneArgument`."""
        def __init__(self, native):
            super().__init__(native)
    
        @staticmethod
        def create(arg: int) -> CtorLinks.SingleCtorWithOneArgument:
            native_result = generated.smoke_CtorLinks.SingleCtorWithOneArgument.create(_unwrap(arg, int))
            return _get_or_create_wrapper(native_result, CtorLinks.SingleCtorWithOneArgument)
    
    
    
    class SingleCtorWithTwoArgument(_NativeBase):
        """This class has just one constructor with two argument `CtorLinks.SingleCtorWithTwoArgument`."""
        def __init__(self, native):
            super().__init__(native)
    
        @staticmethod
        def create(arg: int, arg2: str) -> CtorLinks.SingleCtorWithTwoArgument:
            native_result = generated.smoke_CtorLinks.SingleCtorWithTwoArgument.create(_unwrap(arg, int), _unwrap(arg2, str))
            return _get_or_create_wrapper(native_result, CtorLinks.SingleCtorWithTwoArgument)
    
    
    
    class OverloadedCtors(_NativeBase):
        def __init__(self, native):
            super().__init__(native)
    
        @staticmethod
        def create(*args, **kwargs) -> CtorLinks.OverloadedCtors:
            native_result = generated.smoke_CtorLinks.OverloadedCtors.create(*[_unwrap(a) for a in args])
            return _get_or_create_wrapper(native_result, CtorLinks.OverloadedCtors)
    
    
    

