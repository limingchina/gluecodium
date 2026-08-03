

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase
from enum import Enum
from typing import Optional
import generated


class Constructors(generated.smoke_Constructors):
    def __init__(self, native=None):
        # Subclass the native pybind11 type so a Python override of an inherited virtual
        # method (from a parent interface or open base class) is dispatched through the
        # generated trampoline. When `native` is an existing native instance (returned by
        # a factory), adopt it via the generated adoption constructor; otherwise construct a
        # fresh trampoline. `self._native` aliases the wrapper itself so the rest of the
        # generated code can reach the native object uniformly.
        if native is not None and isinstance(native, generated.smoke_Constructors):
            super().__init__(native)
        else:
            super().__init__()
        self._native = self

    @staticmethod
    def create(*args, **kwargs) -> Constructors:
        native_result = generated.smoke_Constructors.create(*[_unwrap(a) for a in args])
        return _get_or_create_wrapper(native_result, Constructors)






    class ErrorEnum(Enum):
    
        NONE = generated.smoke_ConstructorsErrorEnum.NONE
        CRASHED = generated.smoke_ConstructorsErrorEnum.CRASHED
    
        @property
        def _native(self):
            return self.value
    
    
    
    class ConstructorExplodedError(Exception):
    
        def __init__(self, message: str):
            super().__init__(message)
            self.message = message
    
    

