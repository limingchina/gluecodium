

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase
from enum import Enum
from typing import Optional
import generated

from smoke.ParentInterface import ParentInterface

class CrossPackageChildClass(generated.foobar_CrossPackageChildClass):
    def __init__(self, native=None):
        # Subclass the native pybind11 type so a Python override of an inherited virtual
        # method (from a parent interface or open base class) is dispatched through the
        # generated trampoline. When `native` is an existing native instance (returned by
        # a factory), adopt it via the generated adoption constructor and retain the original
        # native object for calls back into C++; otherwise construct a fresh trampoline.
        if native is not None and isinstance(native, generated.foobar_CrossPackageChildClass):
            super().__init__(native)
            self._native = native
        else:
            super().__init__()
            self._native = self

    def root_method(self):
        return _wrap(generated.foobar_CrossPackageChildClass.root_method(self), None)

    @property
    def root_property(self) -> str:
        return _wrap(generated.foobar_CrossPackageChildClass.root_property.fget(self), str)

    @root_property.setter
    def root_property(self, value: str):
        generated.foobar_CrossPackageChildClass.root_property.fset(self, _unwrap(value, str))


