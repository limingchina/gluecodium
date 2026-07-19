

from __future__ import annotations

from another.SomeCoolClassType import SomeCoolClassType


import generated


class ParentInterface(generated.ParentInterface):
    """"""

    def __init__(self, native=None):
        # Subclass the native pybind11 type so that a Python override of an interface
        # method is dispatched through the generated trampoline. When `native` is an
        # existing native instance (returned by a factory), adopt it via the generated
        # adoption constructor; otherwise construct a fresh trampoline. `self._native`
        # aliases the wrapper itself so the rest of the generated code can reach the
        # native object uniformly (e.g. when passing this interface back into a C++
        # call site).
        if native is not None and isinstance(native, generated.ParentInterface):
            super().__init__(native)
        else:
            super().__init__()
        self._native = self

    def parent_function(self):
        """"""
        return generated.ParentInterface.parent_function(self)

    def some_function_that_uses_type_from_another_package(self, some_param: SomeCoolClassType):
        """"""
        return generated.ParentInterface.some_function_that_uses_type_from_another_package(self, some_param._native)

    @property
    def parent_property(self) -> str:
        """"""
        return generated.ParentInterface.parent_property.fget(self)

    @parent_property.setter
    def parent_property(self, value: str):
        generated.ParentInterface.parent_property.fset(self, value)

