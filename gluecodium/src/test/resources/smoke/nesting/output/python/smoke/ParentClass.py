

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper
from typing import Optional


import generated


class ParentClass(generated.smoke_ParentClass):
    """"""

    def __init__(self, native=None):
        # Subclass the native pybind11 type so a Python override of an inherited virtual
        # method (from a parent interface or open base class) is dispatched through the
        # generated trampoline. When `native` is an existing native instance (returned by
        # a factory), adopt it via the generated adoption constructor; otherwise construct a
        # fresh trampoline. `self._native` aliases the wrapper itself so the rest of the
        # generated code can reach the native object uniformly.
        if native is not None and isinstance(native, generated.smoke_ParentClass):
            super().__init__(native)
        else:
            super().__init__()
        self._native = self

    def parent_fun(self):
        """"""
        return _wrap(generated.smoke_ParentClass.parent_fun(self), None)

    @property
    def parent_property(self) -> str:
        """"""
        return _wrap(generated.smoke_ParentClass.parent_property.fget(self), str)

    @parent_property.setter
    def parent_property(self, value: str):
        generated.smoke_ParentClass.parent_property.fset(self, _unwrap(value, str))

