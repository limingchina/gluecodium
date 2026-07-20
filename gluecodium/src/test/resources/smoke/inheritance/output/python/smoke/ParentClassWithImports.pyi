

from smoke.IncludableClass import IncludableClass
from smoke.IncludableEnum import IncludableEnum
from smoke.IncludableLambda import IncludableLambda
from smoke.IncludableStruct import IncludableStruct
import typing

import generated


class ParentClassWithImports(generated.ParentClassWithImports):
    """"""

    def __init__(self, native=None):
        # Subclass the native pybind11 type so a Python override of an inherited virtual
        # method (from a parent interface or open base class) is dispatched through the
        # generated trampoline. When `native` is an existing native instance (returned by
        # a factory), adopt it via the generated adoption constructor; otherwise construct a
        # fresh trampoline. `self._native` aliases the wrapper itself so the rest of the
        # generated code can reach the native object uniformly.
        if native is not None and isinstance(native, generated.ParentClassWithImports):
            super().__init__(native)
        else:
            super().__init__()
        self._native = self

    def root_method(self, input1: IncludableStruct, input2: IncludableEnum) -> IncludableClass: ...

    @property
    def root_property(self) -> IncludableLambda:
        """"""
        return generated.ParentClassWithImports.root_property.fget(self)

    @root_property.setter
    def root_property(self, value: IncludableLambda):
        generated.ParentClassWithImports.root_property.fset(self, value)

