

from smoke.IncludableClass import IncludableClass
from smoke.IncludableEnum import IncludableEnum
from smoke.IncludableLambda import IncludableLambda
from smoke.IncludableStruct import IncludableStruct
import typing
from typing import Callable

import generated


class ParentClassWithImports(generated.smoke_ParentClassWithImports):
    """"""

    def __init__(self, native=None):
        # Subclass the native pybind11 type so a Python override of an inherited virtual
        # method (from a parent interface or open base class) is dispatched through the
        # generated trampoline. When `native` is an existing native instance (returned by
        # a factory), adopt it via the generated adoption constructor; otherwise construct a
        # fresh trampoline. `self._native` aliases the wrapper itself so the rest of the
        # generated code can reach the native object uniformly.
        if native is not None and isinstance(native, generated.smoke_ParentClassWithImports):
            super().__init__(native)
        else:
            super().__init__()
        self._native = self

    def root_method(self, input1: IncludableStruct, input2: IncludableEnum) -> IncludableClass: ...

    @property
    def root_property(self) -> Callable[[int], None]:
        """"""
        return _wrap(generated.smoke_ParentClassWithImports.root_property.fget(self), Callable[[int], None])

    @root_property.setter
    def root_property(self, value: Callable[[int], None]):
        generated.smoke_ParentClassWithImports.root_property.fset(self, _unwrap(value, Callable[[int], None]))

