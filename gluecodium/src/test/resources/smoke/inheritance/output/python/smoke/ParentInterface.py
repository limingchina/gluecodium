

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase
from enum import Enum
from typing import Optional
import generated


class ParentInterface(generated.smoke_ParentInterface):
    def __init__(self, native=None):
        # Subclass the native pybind11 type so that a Python override of an interface
        # method is dispatched through the generated trampoline. When `native` is an
        # existing native instance (returned by a factory), adopt it via the generated
        # adoption constructor and retain the original native object for calls back into
        # C++; otherwise construct a fresh trampoline.
        if native is not None and isinstance(native, generated.smoke_ParentInterface):
            super().__init__(native)
            self._native = native
        else:
            super().__init__()
            self._native = self

    def root_method(self):
        return _wrap(generated.smoke_ParentInterface.root_method(self), None)

    @property
    def root_property(self) -> str:
        return _wrap(generated.smoke_ParentInterface.root_property.fget(self), str)

    @root_property.setter
    def root_property(self, value: str):
        generated.smoke_ParentInterface.root_property.fset(self, _unwrap(value, str))


