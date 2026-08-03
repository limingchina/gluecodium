

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase
from enum import Enum
from typing import Optional
import generated

from smoke.ParentClass import ParentClass

class OuterClassWithInheritance(generated.smoke_OuterClassWithInheritance):
    def __init__(self, native=None):
        # Subclass the native pybind11 type so a Python override of an inherited virtual
        # method (from a parent interface or open base class) is dispatched through the
        # generated trampoline. When `native` is an existing native instance (returned by
        # a factory), adopt it via the generated adoption constructor; otherwise construct a
        # fresh trampoline. `self._native` aliases the wrapper itself so the rest of the
        # generated code can reach the native object uniformly.
        if native is not None and isinstance(native, generated.smoke_OuterClassWithInheritance):
            super().__init__(native)
        else:
            super().__init__()
        self._native = self

    def foo(self, input: str) -> str:
        return _wrap(generated.smoke_OuterClassWithInheritance.foo(self, _unwrap(input, str)), str)

    class InnerClass(_NativeBase):
        def __init__(self, native):
            super().__init__(native)
    
        def bar(self, input: str) -> str:
            return _wrap(self._native.bar(_unwrap(input, str)), str)
    
    
    
    class InnerInterface(generated.smoke_OuterClassWithInheritance.InnerInterface):
        def __init__(self, native=None):
            # Subclass the native pybind11 type so that a Python override of an interface
            # method is dispatched through the generated trampoline. When `native` is an
            # existing native instance (returned by a factory), adopt it via the generated
            # adoption constructor; otherwise construct a fresh trampoline. `self._native`
            # aliases the wrapper itself so the rest of the generated code can reach the
            # native object uniformly (e.g. when passing this interface back into a C++
            # call site).
            if native is not None and isinstance(native, generated.smoke_OuterClassWithInheritance.InnerInterface):
                super().__init__(native)
            else:
                super().__init__()
            self._native = self
    
        def baz(self, input: str) -> str:
            return _wrap(generated.smoke_OuterClassWithInheritance.InnerInterface.baz(self, _unwrap(input, str)), str)
    
    

