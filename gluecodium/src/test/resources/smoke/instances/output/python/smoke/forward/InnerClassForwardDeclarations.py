

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase
from enum import Enum
from typing import Optional
import generated


class InnerClassForwardDeclarations(_NativeBase):
    def __init__(self, native):
        super().__init__(native)

    class InnerClass1(generated.smoke_forward_InnerClassForwardDeclarations.InnerClass1):
        def __init__(self, native=None):
            # Subclass the native pybind11 type so a Python override of an inherited virtual
            # method (from a parent interface or open base class) is dispatched through the
            # generated trampoline. When `native` is an existing native instance (returned by
            # a factory), adopt it via the generated adoption constructor; otherwise construct a
            # fresh trampoline. `self._native` aliases the wrapper itself so the rest of the
            # generated code can reach the native object uniformly.
            if native is not None and isinstance(native, generated.smoke_forward_InnerClassForwardDeclarations.InnerClass1):
                super().__init__(native)
            else:
                super().__init__()
            self._native = self
    
        def _get_inner_interface(self) -> InnerClassForwardDeclarations._InnerInterface1:
            return _wrap(generated.smoke_forward_InnerClassForwardDeclarations.InnerClass1._get_inner_interface(self), InnerClassForwardDeclarations._InnerInterface1)
    
    
    
    class InnerClass2(_NativeBase):
        def __init__(self, native):
            super().__init__(native)
    
        class InnerInnerClass1(_NativeBase):
            def __init__(self, native):
                super().__init__(native)
    
            def foo(self) -> InnerClassForwardDeclarations.InnerClass2.InnerInnerClass2:
                return _wrap(self._native.foo(), InnerClassForwardDeclarations.InnerClass2.InnerInnerClass2)
    
    
    
        class InnerInnerClass2(_NativeBase):
            def __init__(self, native):
                super().__init__(native)
    
            def bar(self, arg: InnerClassForwardDeclarations.InnerInterface2):
                return _wrap(self._native.bar(_unwrap(arg, InnerClassForwardDeclarations.InnerInterface2)), None)
    
    
    
    
    class _InnerInterface1(generated.smoke_forward_InnerClassForwardDeclarations._InnerInterface1):
        def __init__(self, native=None):
            # Subclass the native pybind11 type so that a Python override of an interface
            # method is dispatched through the generated trampoline. When `native` is an
            # existing native instance (returned by a factory), adopt it via the generated
            # adoption constructor; otherwise construct a fresh trampoline. `self._native`
            # aliases the wrapper itself so the rest of the generated code can reach the
            # native object uniformly (e.g. when passing this interface back into a C++
            # call site).
            if native is not None and isinstance(native, generated.smoke_forward_InnerClassForwardDeclarations._InnerInterface1):
                super().__init__(native)
            else:
                super().__init__()
            self._native = self
    
    
    
    class InnerInterface2(generated.smoke_forward_InnerClassForwardDeclarations.InnerInterface2):
        def __init__(self, native=None):
            # Subclass the native pybind11 type so that a Python override of an interface
            # method is dispatched through the generated trampoline. When `native` is an
            # existing native instance (returned by a factory), adopt it via the generated
            # adoption constructor; otherwise construct a fresh trampoline. `self._native`
            # aliases the wrapper itself so the rest of the generated code can reach the
            # native object uniformly (e.g. when passing this interface back into a C++
            # call site).
            if native is not None and isinstance(native, generated.smoke_forward_InnerClassForwardDeclarations.InnerInterface2):
                super().__init__(native)
            else:
                super().__init__()
            self._native = self
    
    
    
    class InnerInterface3(generated.smoke_forward_InnerClassForwardDeclarations.InnerInterface3):
        def __init__(self, native=None):
            # Subclass the native pybind11 type so that a Python override of an interface
            # method is dispatched through the generated trampoline. When `native` is an
            # existing native instance (returned by a factory), adopt it via the generated
            # adoption constructor; otherwise construct a fresh trampoline. `self._native`
            # aliases the wrapper itself so the rest of the generated code can reach the
            # native object uniformly (e.g. when passing this interface back into a C++
            # call site).
            if native is not None and isinstance(native, generated.smoke_forward_InnerClassForwardDeclarations.InnerInterface3):
                super().__init__(native)
            else:
                super().__init__()
            self._native = self
    
    

