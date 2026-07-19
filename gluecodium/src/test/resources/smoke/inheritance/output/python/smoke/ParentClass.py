

from __future__ import annotations


import generated


class ParentClass(generated.ParentClass):
    """"""

    def __init__(self, native=None):
        # Subclass the native pybind11 type so a Python override of an inherited virtual
        # method (from a parent interface or open base class) is dispatched through the
        # generated trampoline. When `native` is an existing native instance (returned by
        # a factory), adopt it via the generated adoption constructor; otherwise construct a
        # fresh trampoline. `self._native` aliases the wrapper itself so the rest of the
        # generated code can reach the native object uniformly.
        if native is not None and isinstance(native, generated.ParentClass):
            super().__init__(native)
        else:
            super().__init__()
        self._native = self

    def root_method(self):
        """"""
        return generated.ParentClass.root_method(self)

    @property
    def root_property(self) -> str:
        """"""
        return generated.ParentClass.root_property.fget(self)

    @root_property.setter
    def root_property(self, value: str):
        generated.ParentClass.root_property.fset(self, value)

