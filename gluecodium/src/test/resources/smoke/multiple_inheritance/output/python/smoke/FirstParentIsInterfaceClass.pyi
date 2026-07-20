

from another.SomeCoolClassType import SomeCoolClassType
from smoke.ParentInterface import ParentInterface
from smoke.ParentNarrowOne import ParentNarrowOne
import typing

import generated


class FirstParentIsInterfaceClass(generated.FirstParentIsInterfaceClass):
    """"""

    def __init__(self, native=None):
        # Subclass the native pybind11 type so a Python override of an inherited virtual
        # method (from a parent interface or open base class) is dispatched through the
        # generated trampoline. When `native` is an existing native instance (returned by
        # a factory), adopt it via the generated adoption constructor; otherwise construct a
        # fresh trampoline. `self._native` aliases the wrapper itself so the rest of the
        # generated code can reach the native object uniformly.
        if native is not None and isinstance(native, generated.FirstParentIsInterfaceClass):
            super().__init__(native)
        else:
            super().__init__()
        self._native = self

    def child_function(self): ...

    @property
    def child_property(self) -> str:
        """"""
        return generated.FirstParentIsInterfaceClass.child_property.fget(self)

    @child_property.setter
    def child_property(self, value: str):
        generated.FirstParentIsInterfaceClass.child_property.fset(self, value)

