

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase
from enum import Enum
from typing import Optional
import generated

from smoke.ParentInterface import ParentInterface

class ChildInterfaceOverloads(generated.smoke_ChildInterfaceOverloads):
    def __init__(self, native=None):
        # Subclass the native pybind11 type so that a Python override of an interface
        # method is dispatched through the generated trampoline. When `native` is an
        # existing native instance (returned by a factory), adopt it via the generated
        # adoption constructor; otherwise construct a fresh trampoline. `self._native`
        # aliases the wrapper itself so the rest of the generated code can reach the
        # native object uniformly (e.g. when passing this interface back into a C++
        # call site).
        if native is not None and isinstance(native, generated.smoke_ChildInterfaceOverloads):
            super().__init__(native)
        else:
            super().__init__()
        self._native = self

    def foo(self, input: str):
        return _wrap(generated.smoke_ChildInterfaceOverloads.foo(self, _unwrap(input, str)), None)

    def bar(self, input: str):
        return _wrap(generated.smoke_ChildInterfaceOverloads.bar(self, _unwrap(input, str)), None)


