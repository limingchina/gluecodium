

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
        # a factory), adopt it via the generated adoption constructor and retain the original
        # native object for calls back into C++; otherwise construct a fresh trampoline.
        if native is not None and isinstance(native, generated.smoke_Constructors):
            super().__init__(native)
            self._native = native
        else:
            super().__init__()
            self._native = self

    @staticmethod
    def create(*args, **kwargs) -> Constructors:
        native_result = generated.smoke_Constructors.create(*[_unwrap(a) for a in args])
        return _get_or_create_wrapper(native_result, Constructors)






    class ErrorEnum(Enum):
    
        NONE = generated.smoke_Constructors.ErrorEnum.NONE
        CRASHED = generated.smoke_Constructors.ErrorEnum.CRASHED
    
        @property
        def _native(self):
            return self.value
    
    
    
    class ConstructorExplodedError(Exception):
    
        def __init__(self, message: str):
            super().__init__(message)
            self.message = message
    
    

