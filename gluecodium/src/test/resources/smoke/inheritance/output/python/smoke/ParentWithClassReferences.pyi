

from smoke.ChildClassFromClass import ChildClassFromClass
from smoke.ParentClass import ParentClass


import generated


class ParentWithClassReferences(generated.ParentWithClassReferences):
    """"""

    def __init__(self, native=None):
        # Subclass the native pybind11 type so that a Python override of an interface
        # method is dispatched through the generated trampoline. When `native` is an
        # existing native instance (returned by a factory), adopt it via the generated
        # adoption constructor; otherwise construct a fresh trampoline. `self._native`
        # aliases the wrapper itself so the rest of the generated code can reach the
        # native object uniformly (e.g. when passing this interface back into a C++
        # call site).
        if native is not None and isinstance(native, generated.ParentWithClassReferences):
            super().__init__(native)
        else:
            super().__init__()
        self._native = self

    def class_function(self) -> ChildClassFromClass:
        """"""
        return generated.ParentWithClassReferences.class_function(self)

    @property
    def class_property(self) -> ParentClass:
        """"""
        return generated.ParentWithClassReferences.class_property.fget(self)

    @class_property.setter
    def class_property(self, value: ParentClass):
        generated.ParentWithClassReferences.class_property.fset(self, value)

