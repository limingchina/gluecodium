

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase
from enum import Enum
from typing import Optional
import generated

from smoke.PublicClass import PublicClass

class PublicInterface(generated.smoke_PublicInterface):
    def __init__(self, native=None):
        # Subclass the native pybind11 type so that a Python override of an interface
        # method is dispatched through the generated trampoline. When `native` is an
        # existing native instance (returned by a factory), adopt it via the generated
        # adoption constructor; otherwise construct a fresh trampoline. `self._native`
        # aliases the wrapper itself so the rest of the generated code can reach the
        # native object uniformly (e.g. when passing this interface back into a C++
        # call site).
        if native is not None and isinstance(native, generated.smoke_PublicInterface):
            super().__init__(native)
        else:
            super().__init__()
        self._native = self

    class _InternalStruct(_NativeBase):
        def __init__(self, *args, **kwargs):
            if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_PublicInterface._InternalStruct):
                super().__init__(args[0])
            else:
                super().__init__(generated.smoke_PublicInterface._InternalStruct(
                    *[_unwrap(arg) for arg in args],
                    **{k: _unwrap(v) for k, v in kwargs.items()}
                ))
    
        @property
        def field_of_internal_type(self) -> PublicClass._InternalStruct:
            return _wrap(self._native.field_of_internal_type, PublicClass._InternalStruct)
        @field_of_internal_type.setter
        def field_of_internal_type(self, value: PublicClass._InternalStruct):
          self._native.field_of_internal_type = _unwrap(value, PublicClass._InternalStruct)
    
    
    

