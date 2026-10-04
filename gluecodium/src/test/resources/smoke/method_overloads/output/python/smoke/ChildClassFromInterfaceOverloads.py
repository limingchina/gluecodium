

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase
from enum import Enum
from typing import Optional
import generated

from smoke.ParentInterface import ParentInterface

class ChildClassFromInterfaceOverloads(generated.smoke_ChildClassFromInterfaceOverloads):
    def __init__(self, native=None):
        # Subclass the native pybind11 type so a Python override of an inherited virtual
        # method (from a parent interface or open base class) is dispatched through the
        # generated trampoline. When `native` is an existing native instance (returned by
        # a factory), adopt it via the generated adoption constructor and retain the original
        # native object for calls back into C++; otherwise construct a fresh trampoline.
        if native is not None and isinstance(native, generated.smoke_ChildClassFromInterfaceOverloads):
            super().__init__(native)
            self._native = native
        else:
            super().__init__()
            self._native = self

    def foo(self, *args, **kwargs):
        return _wrap(generated.smoke_ChildClassFromInterfaceOverloads.foo(self, *[_unwrap(a) for a in args]), None)


    def bar(self, *args, **kwargs):
        return _wrap(generated.smoke_ChildClassFromInterfaceOverloads.bar(self, *[_unwrap(a) for a in args]), None)


    def foo(self, *args, **kwargs):
        return _wrap(generated.smoke_ChildClassFromInterfaceOverloads.foo(self, *[_unwrap(a) for a in args]), None)


    def bar(self):
        return _wrap(generated.smoke_ChildClassFromInterfaceOverloads.bar(self), None)

    def baz(self):
        return _wrap(generated.smoke_ChildClassFromInterfaceOverloads.baz(self), None)


