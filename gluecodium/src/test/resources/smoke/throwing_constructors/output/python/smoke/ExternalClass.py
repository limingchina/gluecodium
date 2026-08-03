

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase
from enum import Enum
from typing import Optional
import generated


class ExternalClass(generated.smoke_ExternalClass):
    def __init__(self, native=None):
        # Subclass the native pybind11 type so a Python override of an inherited virtual
        # method (from a parent interface or open base class) is dispatched through the
        # generated trampoline. When `native` is an existing native instance (returned by
        # a factory), adopt it via the generated adoption constructor; otherwise construct a
        # fresh trampoline. `self._native` aliases the wrapper itself so the rest of the
        # generated code can reach the native object uniformly.
        if native is not None and isinstance(native, generated.smoke_ExternalClass):
            super().__init__(native)
        else:
            super().__init__()
        self._native = self

    @staticmethod
    def create() -> ExternalClass:
        native_result = generated.smoke_ExternalClass.create()
        return _get_or_create_wrapper(native_result, ExternalClass)

    class InternalOne(_NativeBase):
        def __init__(self, native):
            super().__init__(native)
    
        @staticmethod
        def create(*args, **kwargs) -> ExternalClass.InternalOne:
            native_result = generated.smoke_ExternalClassInternalOne.create(*[_unwrap(a) for a in args])
            return _get_or_create_wrapper(native_result, ExternalClass.InternalOne)
    
    
    
    
    class InternalTwo(_NativeBase):
        def __init__(self, native):
            super().__init__(native)
    
        @staticmethod
        def create() -> ExternalClass.InternalTwo:
            native_result = generated.smoke_ExternalClassInternalTwo.create()
            return _get_or_create_wrapper(native_result, ExternalClass.InternalTwo)
    
    
    
    class ErrorEnum(Enum):
    
        NONE = generated.smoke_ExternalClassErrorEnum.NONE
        CRASHED = generated.smoke_ExternalClassErrorEnum.CRASHED
    
        @property
        def _native(self):
            return self.value
    
    
    
    class ConstructorExplodedError(Exception):
    
        def __init__(self, message: str):
            super().__init__(message)
            self.message = message
    
    

