

from smoke.IncludableClass import IncludableClass
from smoke.IncludableEnum import IncludableEnum
from smoke.IncludableLambda import IncludableLambda
from smoke.IncludableStruct import IncludableStruct
from smoke.ShouldNotInclude import ShouldNotInclude
import typing


import generated


class ParentInterfaceWithIncludes(generated.ParentInterfaceWithIncludes):
    """"""

    def __init__(self, native=None):
        # Subclass the native pybind11 type so that a Python override of an interface
        # method is dispatched through the generated trampoline. When `native` is an
        # existing native instance (returned by a factory), adopt it via the generated
        # adoption constructor; otherwise construct a fresh trampoline. `self._native`
        # aliases the wrapper itself so the rest of the generated code can reach the
        # native object uniformly (e.g. when passing this interface back into a C++
        # call site).
        if native is not None and isinstance(native, generated.ParentInterfaceWithIncludes):
            super().__init__(native)
        else:
            super().__init__()
        self._native = self

    def root_method(self, input1: IncludableStruct, input2: IncludableEnum) -> IncludableClass: ...

    def not_in_java(self) -> ShouldNotInclude: ...

    @property
    def root_property(self) -> IncludableLambda:
        """"""
        return _wrap(generated.ParentInterfaceWithIncludes.root_property.fget(self), IncludableLambda)

    @root_property.setter
    def root_property(self, value: IncludableLambda):
        generated.ParentInterfaceWithIncludes.root_property.fset(self, _unwrap(value, IncludableLambda))

    @property
    def not_in_java_property(self) -> ShouldNotInclude:
        """"""
        return _wrap(generated.ParentInterfaceWithIncludes.not_in_java_property.fget(self), ShouldNotInclude)

    @not_in_java_property.setter
    def not_in_java_property(self, value: ShouldNotInclude):
        generated.ParentInterfaceWithIncludes.not_in_java_property.fset(self, _unwrap(value, ShouldNotInclude))

