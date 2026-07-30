

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper
from typing import Optional



import generated


class InterfaceWithStatic(generated.smoke_InterfaceWithStatic):
    def __init__(self, native=None):
        # Subclass the native pybind11 type so that a Python override of an interface
        # method is dispatched through the generated trampoline. When `native` is an
        # existing native instance (returned by a factory), adopt it via the generated
        # adoption constructor; otherwise construct a fresh trampoline. `self._native`
        # aliases the wrapper itself so the rest of the generated code can reach the
        # native object uniformly (e.g. when passing this interface back into a C++
        # call site).
        if native is not None and isinstance(native, generated.smoke_InterfaceWithStatic):
            super().__init__(native)
        else:
            super().__init__()
        self._native = self

    def regular_function(self) -> str:
        return _wrap(generated.smoke_InterfaceWithStatic.regular_function(self), str)

    @staticmethod
    def static_function() -> str:
        return generated.smoke_InterfaceWithStatic.static_function()

    @property
    def regular_property(self) -> str:
        return _wrap(generated.smoke_InterfaceWithStatic.regular_property.fget(self), str)

    @regular_property.setter
    def regular_property(self, value: str):
        generated.smoke_InterfaceWithStatic.regular_property.fset(self, _unwrap(value, str))

    @staticmethod
    def static_property() -> str:
        return _wrap(generated.smoke_InterfaceWithStatic.static_property(), str)

    @staticmethod
    def static_property_set(value: str):
        generated.smoke_InterfaceWithStatic.static_property_set(_unwrap(value, str))

