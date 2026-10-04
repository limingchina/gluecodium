

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

@_mark_callback_base
class ParentClassWithImports(generated.smoke_ParentClassWithImports):
    @classmethod
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        _install_callback_adapters(cls, __class__, [
            ("root_method", "__gluecodium_callback_736d6f6b652e506172656e74436c61737357697468496d706f7274732e726f6f744d6574686f64", "method", None,
             lambda: ([IncludableStruct, IncludableEnum], IncludableClass)),
            ("root_property", "__gluecodium_callback_736d6f6b652e506172656e74436c61737357697468496d706f7274732e726f6f7450726f7065727479_get", "get", "get_root_property",
             lambda: ([], Callable[[int], None])),
            ("root_property", "__gluecodium_callback_736d6f6b652e506172656e74436c61737357697468496d706f7274732e726f6f7450726f7065727479_set", "set", "set_root_property",
             lambda: ([Callable[[int], None]], None)),
        ])
    def __init__(self, native=None):
        # Subclass the native pybind11 type so a Python override of an inherited virtual
        # method (from a parent interface or open base class) is dispatched through the
        # generated trampoline. When `native` is an existing native instance (returned by
        # a factory), adopt it via the generated adoption constructor and retain the original
        # native object for calls back into C++; otherwise construct a fresh trampoline.
        if native is not None and isinstance(native, generated.smoke_ParentClassWithImports):
            super().__init__(native)
            self._native = native
        else:
            super().__init__()
            self._native = self

    def root_method(self, input1: IncludableStruct, input2: IncludableEnum) -> IncludableClass:
        return _wrap(generated.smoke_ParentClassWithImports.root_method(self, _unwrap(input1, IncludableStruct), _unwrap(input2, IncludableEnum)), IncludableClass)

    @property
    def root_property(self) -> Callable[[int], None]:
        return _wrap(generated.smoke_ParentClassWithImports.root_property.fget(self), Callable[[int], None])

    @root_property.setter
    def root_property(self, value: Callable[[int], None]):
        generated.smoke_ParentClassWithImports.root_property.fset(self, _unwrap(value, Callable[[int], None]))
