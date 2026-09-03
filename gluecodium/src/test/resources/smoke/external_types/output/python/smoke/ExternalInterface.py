

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase
from enum import Enum
from typing import Optional
import generated


class ExternalInterface(generated.smoke_ExternalInterface):
    def __init__(self, native=None):
        # Subclass the native pybind11 type so that a Python override of an interface
        # method is dispatched through the generated trampoline. When `native` is an
        # existing native instance (returned by a factory), adopt it via the generated
        # adoption constructor; otherwise construct a fresh trampoline. `self._native`
        # aliases the wrapper itself so the rest of the generated code can reach the
        # native object uniformly (e.g. when passing this interface back into a C++
        # call site).
        if native is not None and isinstance(native, generated.smoke_ExternalInterface):
            super().__init__(native)
        else:
            super().__init__()
        self._native = self

    def some_method(self, some_parameter: int):
        return _wrap(generated.smoke_ExternalInterface.some_method(self, _unwrap(some_parameter, int)), None)

    @property
    def some_property(self) -> str:
        return _wrap(generated.smoke_ExternalInterface.some_property.fget(self), str)


    class SomeStruct(_NativeBase):
        def __init__(self, *args, **kwargs):
            if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_ExternalInterface.SomeStruct):
                super().__init__(args[0])
            else:
                super().__init__(generated.smoke_ExternalInterface.SomeStruct(
                    *[_unwrap(arg) for arg in args],
                    **{k: _unwrap(v) for k, v in kwargs.items()}
                ))
    
        @property
        def some_field(self) -> str:
            return _wrap(self._native.some_field, str)
        @some_field.setter
        def some_field(self, value: str):
          self._native.some_field = _unwrap(value, str)
    
    
    
    
    class SomeEnum(Enum):
    
        SOME_VALUE = generated.smoke_ExternalInterface.SomeEnum.SOME_VALUE
    
        @property
        def _native(self):
            return self.value
    
    

