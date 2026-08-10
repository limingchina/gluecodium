

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase
from enum import Enum
from typing import Optional
import generated

from smoke.IncludableClass import IncludableClass
from smoke.IncludableEnum import IncludableEnum
from smoke.IncludableLambda import IncludableLambda
from smoke.IncludableStruct import IncludableStruct
from smoke.ParentInterfaceWithIncludes import ParentInterfaceWithIncludes
from smoke.ShouldNotInclude import ShouldNotInclude

class ChildClassWithIncludes(generated.smoke_ChildClassWithIncludes):
    def __init__(self, native=None):
        # Subclass the native pybind11 type so a Python override of an inherited virtual
        # method (from a parent interface or open base class) is dispatched through the
        # generated trampoline. When `native` is an existing native instance (returned by
        # a factory), adopt it via the generated adoption constructor; otherwise construct a
        # fresh trampoline. `self._native` aliases the wrapper itself so the rest of the
        # generated code can reach the native object uniformly.
        if native is not None and isinstance(native, generated.smoke_ChildClassWithIncludes):
            super().__init__(native)
        else:
            super().__init__()
        self._native = self

    def root_method(self, input1: IncludableStruct, input2: IncludableEnum) -> IncludableClass:
        return _wrap(generated.smoke_ChildClassWithIncludes.root_method(self, _unwrap(input1, IncludableStruct), _unwrap(input2, IncludableEnum)), IncludableClass)

    def not_in_java(self) -> ShouldNotInclude:
        return _wrap(generated.smoke_ChildClassWithIncludes.not_in_java(self), ShouldNotInclude)

    @property
    def root_property(self) -> Callable[[int], None]:
        return _wrap(generated.smoke_ChildClassWithIncludes.root_property.fget(self), Callable[[int], None])

    @root_property.setter
    def root_property(self, value: Callable[[int], None]):
        generated.smoke_ChildClassWithIncludes.root_property.fset(self, _unwrap(value, Callable[[int], None]))

    @property
    def not_in_java_property(self) -> ShouldNotInclude:
        return _wrap(generated.smoke_ChildClassWithIncludes.not_in_java_property.fget(self), ShouldNotInclude)

    @not_in_java_property.setter
    def not_in_java_property(self, value: ShouldNotInclude):
        generated.smoke_ChildClassWithIncludes.not_in_java_property.fset(self, _unwrap(value, ShouldNotInclude))


