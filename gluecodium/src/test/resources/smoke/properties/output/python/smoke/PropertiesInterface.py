

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase
from enum import Enum
from typing import Optional
import generated


class PropertiesInterface(generated.smoke_PropertiesInterface):
    def __init__(self, native=None):
        # Subclass the native pybind11 type so that a Python override of an interface
        # method is dispatched through the generated trampoline. When `native` is an
        # existing native instance (returned by a factory), adopt it via the generated
        # adoption constructor; otherwise construct a fresh trampoline. `self._native`
        # aliases the wrapper itself so the rest of the generated code can reach the
        # native object uniformly (e.g. when passing this interface back into a C++
        # call site).
        if native is not None and isinstance(native, generated.smoke_PropertiesInterface):
            super().__init__(native)
        else:
            super().__init__()
        self._native = self

    @property
    def struct_property(self) -> PropertiesInterface.ExampleStruct:
        return _wrap(generated.smoke_PropertiesInterface.struct_property.fget(self), PropertiesInterface.ExampleStruct)

    @struct_property.setter
    def struct_property(self, value: PropertiesInterface.ExampleStruct):
        generated.smoke_PropertiesInterface.struct_property.fset(self, _unwrap(value, PropertiesInterface.ExampleStruct))

    class ExampleStruct(_NativeBase):
        def __init__(self, *args, **kwargs):
            if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_PropertiesInterface.ExampleStruct):
                super().__init__(args[0])
            else:
                super().__init__(generated.smoke_PropertiesInterface.ExampleStruct(
                    *[_unwrap(arg) for arg in args],
                    **{k: _unwrap(v) for k, v in kwargs.items()}
                ))
    
        @property
        def value(self) -> float:
            return _wrap(self._native.value, float)
        @value.setter
        def value(self, value: float):
          self._native.value = _unwrap(value, float)
    
    
    

