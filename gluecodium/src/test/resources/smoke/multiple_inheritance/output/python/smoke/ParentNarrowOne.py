

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase
from enum import Enum
from typing import Optional
import generated


class ParentNarrowOne(generated.smoke_ParentNarrowOne):
    def __init__(self, native=None):
        # Subclass the native pybind11 type so that a Python override of an interface
        # method is dispatched through the generated trampoline. When `native` is an
        # existing native instance (returned by a factory), adopt it via the generated
        # adoption constructor; otherwise construct a fresh trampoline. `self._native`
        # aliases the wrapper itself so the rest of the generated code can reach the
        # native object uniformly (e.g. when passing this interface back into a C++
        # call site).
        if native is not None and isinstance(native, generated.smoke_ParentNarrowOne):
            super().__init__(native)
        else:
            super().__init__()
        self._native = self

    def parent_function_one(self):
        return _wrap(generated.smoke_ParentNarrowOne.parent_function_one(self), None)

    @property
    def parent_property_one(self) -> str:
        return _wrap(generated.smoke_ParentNarrowOne.parent_property_one.fget(self), str)

    @parent_property_one.setter
    def parent_property_one(self, value: str):
        generated.smoke_ParentNarrowOne.parent_property_one.fset(self, _unwrap(value, str))


