

from __future__ import annotations

from smoke.ParentNarrowOne import ParentNarrowOne
from smoke.ParentNarrowTwo import ParentNarrowTwo


import generated


class FirstParentIsNarrowInterface(generated.FirstParentIsNarrowInterface):
    """"""

    def __init__(self, native=None):
        # Subclass the native pybind11 type so that a Python override of an interface
        # method is dispatched through the generated trampoline. When `native` is an
        # existing native instance (returned by a factory), adopt it via the generated
        # adoption constructor; otherwise construct a fresh trampoline. `self._native`
        # aliases the wrapper itself so the rest of the generated code can reach the
        # native object uniformly (e.g. when passing this interface back into a C++
        # call site).
        if native is not None and isinstance(native, generated.FirstParentIsNarrowInterface):
            super().__init__(native)
        else:
            super().__init__()
        self._native = self

    def child_function(self):
        """"""
        return generated.FirstParentIsNarrowInterface.child_function(self)

    @property
    def child_property(self) -> str:
        """"""
        return generated.FirstParentIsNarrowInterface.child_property.fget(self)

    @child_property.setter
    def child_property(self, value: str):
        generated.FirstParentIsNarrowInterface.child_property.fset(self, value)

