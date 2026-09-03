

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase
from enum import Enum
from typing import Optional
import generated

from smoke.ParentInterfaceWithBool import ParentInterfaceWithBool

class ChildClassWithBool(generated.smoke_ChildClassWithBool):
    def __init__(self, native=None):
        # Subclass the native pybind11 type so a Python override of an inherited virtual
        # method (from a parent interface or open base class) is dispatched through the
        # generated trampoline. When `native` is an existing native instance (returned by
        # a factory), adopt it via the generated adoption constructor; otherwise construct a
        # fresh trampoline. `self._native` aliases the wrapper itself so the rest of the
        # generated code can reach the native object uniformly.
        if native is not None and isinstance(native, generated.smoke_ChildClassWithBool):
            super().__init__(native)
        else:
            super().__init__()
        self._native = self

    def root_method(self, input1: bool):
        return _wrap(generated.smoke_ChildClassWithBool.root_method(self, _unwrap(input1, bool)), None)


