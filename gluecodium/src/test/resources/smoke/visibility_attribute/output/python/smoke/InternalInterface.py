

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional



import generated


class InternalInterface(generated.smoke_InternalInterface):
    """"""

    def __init__(self, native=None):
        # Subclass the native pybind11 type so that a Python override of an interface
        # method is dispatched through the generated trampoline. When `native` is an
        # existing native instance (returned by a factory), adopt it via the generated
        # adoption constructor; otherwise construct a fresh trampoline. `self._native`
        # aliases the wrapper itself so the rest of the generated code can reach the
        # native object uniformly (e.g. when passing this interface back into a C++
        # call site).
        if native is not None and isinstance(native, generated.smoke_InternalInterface):
            super().__init__(native)
        else:
            super().__init__()
        self._native = self

    def foo_bar(self):
        """"""
        return _wrap(generated.smoke_InternalInterface.foo_bar(self), None)


    @staticmethod
    def some_property_of_internal_interface() -> str:
        """"""
        return _wrap(generated.smoke_InternalInterface.some_property_of_internal_interface(), str)

    @staticmethod
    def some_property_of_internal_interface_set(value: str):
        generated.smoke_InternalInterface.some_property_of_internal_interface_set(_unwrap(value, str))

