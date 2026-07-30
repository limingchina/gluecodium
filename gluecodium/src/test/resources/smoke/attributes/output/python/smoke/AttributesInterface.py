

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper
from typing import Optional



import generated


class AttributesInterface(generated.smoke_AttributesInterface):
    def __init__(self, native=None):
        # Subclass the native pybind11 type so that a Python override of an interface
        # method is dispatched through the generated trampoline. When `native` is an
        # existing native instance (returned by a factory), adopt it via the generated
        # adoption constructor; otherwise construct a fresh trampoline. `self._native`
        # aliases the wrapper itself so the rest of the generated code can reach the
        # native object uniformly (e.g. when passing this interface back into a C++
        # call site).
        if native is not None and isinstance(native, generated.smoke_AttributesInterface):
            super().__init__(native)
        else:
            super().__init__()
        self._native = self

    def very_fun(self, param: str):
        return _wrap(generated.smoke_AttributesInterface.very_fun(self, _unwrap(param, str)), None)

    @property
    def prop(self) -> str:
        return _wrap(generated.smoke_AttributesInterface.prop.fget(self), str)

    @prop.setter
    def prop(self, value: str):
        generated.smoke_AttributesInterface.prop.fset(self, _unwrap(value, str))

    PI = False

