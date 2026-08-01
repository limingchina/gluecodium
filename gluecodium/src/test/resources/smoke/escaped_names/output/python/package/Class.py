

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase
from enum import Enum
from typing import Optional
import generated

from package.Interface import Interface
from package.Types import Types

class Class(generated.package_Class):
    def __init__(self, native=None):
        # Subclass the native pybind11 type so a Python override of an inherited virtual
        # method (from a parent interface or open base class) is dispatched through the
        # generated trampoline. When `native` is an existing native instance (returned by
        # a factory), adopt it via the generated adoption constructor; otherwise construct a
        # fresh trampoline. `self._native` aliases the wrapper itself so the rest of the
        # generated code can reach the native object uniformly.
        if native is not None and isinstance(native, generated.package_Class):
            super().__init__(native)
        else:
            super().__init__()
        self._native = self

    @staticmethod
    def constructor() -> Class:
        native_result = generated.package_Class.constructor()
        return _get_or_create_wrapper(native_result, Class)

    def fun(self, double: list[Types.Struct]) -> Types.Struct:
        return _wrap(generated.package_Class.fun(self, _unwrap(double, list[Types.Struct])), Types.Struct)

    @property
    def property(self) -> Types.Enum:
        return _wrap(generated.package_Class.property.fget(self), Types.Enum)

    @property.setter
    def property(self, value: Types.Enum):
        generated.package_Class.property.fset(self, _unwrap(value, Types.Enum))


