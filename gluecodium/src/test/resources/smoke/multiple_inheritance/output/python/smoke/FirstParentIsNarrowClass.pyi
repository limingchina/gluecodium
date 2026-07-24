

from smoke.ParentNarrowOne import ParentNarrowOne
from smoke.ParentNarrowTwo import ParentNarrowTwo
import typing

import generated


class FirstParentIsNarrowClass(generated.FirstParentIsNarrowClass):
    """"""

    def __init__(self, native=None):
        # Subclass the native pybind11 type so a Python override of an inherited virtual
        # method (from a parent interface or open base class) is dispatched through the
        # generated trampoline. When `native` is an existing native instance (returned by
        # a factory), adopt it via the generated adoption constructor; otherwise construct a
        # fresh trampoline. `self._native` aliases the wrapper itself so the rest of the
        # generated code can reach the native object uniformly.
        if native is not None and isinstance(native, generated.FirstParentIsNarrowClass):
            super().__init__(native)
        else:
            super().__init__()
        self._native = self

    def child_function(self): ...

    @property
    def child_property(self) -> str:
        """"""
        return _wrap(generated.FirstParentIsNarrowClass.child_property.fget(self), str)

    @child_property.setter
    def child_property(self, value: str):
        generated.FirstParentIsNarrowClass.child_property.fset(self, _unwrap(value, str))

