

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional

from another.SomeCoolClassType import SomeCoolClassType


import generated


class ParentInterface(generated.smoke_ParentInterface):
    """"""

    def __init__(self, native=None):
        # Subclass the native pybind11 type so that a Python override of an interface
        # method is dispatched through the generated trampoline. When `native` is an
        # existing native instance (returned by a factory), adopt it via the generated
        # adoption constructor; otherwise construct a fresh trampoline. `self._native`
        # aliases the wrapper itself so the rest of the generated code can reach the
        # native object uniformly (e.g. when passing this interface back into a C++
        # call site).
        if native is not None and isinstance(native, generated.smoke_ParentInterface):
            super().__init__(native)
        else:
            super().__init__()
        self._native = self

    def parent_function(self):
        """"""
        return _wrap(generated.smoke_ParentInterface.parent_function(self), None)

    def some_function_that_uses_type_from_another_package(self, some_param: SomeCoolClassType):
        """"""
        return _wrap(generated.smoke_ParentInterface.some_function_that_uses_type_from_another_package(self, _unwrap(some_param, SomeCoolClassType)), None)

    @property
    def parent_property(self) -> str:
        """"""
        return _wrap(generated.smoke_ParentInterface.parent_property.fget(self), str)

    @parent_property.setter
    def parent_property(self, value: str):
        generated.smoke_ParentInterface.parent_property.fset(self, _unwrap(value, str))

