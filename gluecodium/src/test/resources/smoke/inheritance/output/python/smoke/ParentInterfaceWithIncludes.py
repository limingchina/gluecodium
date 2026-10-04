

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase, _install_callback_adapters, _unwrap_struct_args, _mark_callback_base, _struct_key
from enum import Enum
from typing import Optional
from typing import Callable
import generated

from smoke.IncludableClass import IncludableClass
from smoke.IncludableEnum import IncludableEnum
from smoke.IncludableLambda import IncludableLambda
from smoke.IncludableStruct import IncludableStruct
from smoke.ShouldNotInclude import ShouldNotInclude

@_mark_callback_base
class ParentInterfaceWithIncludes(generated.smoke_ParentInterfaceWithIncludes):
    @classmethod
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        _install_callback_adapters(cls, __class__, [
            ("root_method", "__gluecodium_callback_736d6f6b652e506172656e74496e7465726661636557697468496e636c756465732e726f6f744d6574686f64", "method", None,
             lambda: ([IncludableStruct, IncludableEnum], IncludableClass)),
            ("not_in_java", "__gluecodium_callback_736d6f6b652e506172656e74496e7465726661636557697468496e636c756465732e6e6f74496e4a617661", "method", None,
             lambda: ([], ShouldNotInclude)),
            ("root_property", "__gluecodium_callback_736d6f6b652e506172656e74496e7465726661636557697468496e636c756465732e726f6f7450726f7065727479_get", "get", "get_root_property",
             lambda: ([], Callable[[int], None])),
            ("root_property", "__gluecodium_callback_736d6f6b652e506172656e74496e7465726661636557697468496e636c756465732e726f6f7450726f7065727479_set", "set", "set_root_property",
             lambda: ([Callable[[int], None]], None)),
            ("not_in_java_property", "__gluecodium_callback_736d6f6b652e506172656e74496e7465726661636557697468496e636c756465732e6e6f74496e4a61766150726f7065727479_get", "get", "get_not_in_java_property",
             lambda: ([], ShouldNotInclude)),
            ("not_in_java_property", "__gluecodium_callback_736d6f6b652e506172656e74496e7465726661636557697468496e636c756465732e6e6f74496e4a61766150726f7065727479_set", "set", "set_not_in_java_property",
             lambda: ([ShouldNotInclude], None)),
        ])
    def __init__(self, native=None):
        # Subclass the native pybind11 type so that a Python override of an interface
        # method is dispatched through the generated trampoline. When `native` is an
        # existing native instance (returned by a factory), adopt it via the generated
        # adoption constructor and retain the original native object for calls back into
        # C++; otherwise construct a fresh trampoline.
        if native is not None and isinstance(native, generated.smoke_ParentInterfaceWithIncludes):
            super().__init__(native)
            self._native = native
        else:
            super().__init__()
            self._native = self

    def root_method(self, input1: IncludableStruct, input2: IncludableEnum) -> IncludableClass:
        return _wrap(generated.smoke_ParentInterfaceWithIncludes.root_method(self, _unwrap(input1, IncludableStruct), _unwrap(input2, IncludableEnum)), IncludableClass)

    def not_in_java(self) -> ShouldNotInclude:
        return _wrap(generated.smoke_ParentInterfaceWithIncludes.not_in_java(self), ShouldNotInclude)

    @property
    def root_property(self) -> Callable[[int], None]:
        return _wrap(generated.smoke_ParentInterfaceWithIncludes.root_property.fget(self), Callable[[int], None])

    @root_property.setter
    def root_property(self, value: Callable[[int], None]):
        generated.smoke_ParentInterfaceWithIncludes.root_property.fset(self, _unwrap(value, Callable[[int], None]))

    @property
    def not_in_java_property(self) -> ShouldNotInclude:
        return _wrap(generated.smoke_ParentInterfaceWithIncludes.not_in_java_property.fget(self), ShouldNotInclude)

    @not_in_java_property.setter
    def not_in_java_property(self, value: ShouldNotInclude):
        generated.smoke_ParentInterfaceWithIncludes.not_in_java_property.fset(self, _unwrap(value, ShouldNotInclude))
