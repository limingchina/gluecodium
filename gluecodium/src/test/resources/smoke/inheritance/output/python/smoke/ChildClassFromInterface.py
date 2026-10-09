

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase, _install_callback_adapters, _unwrap_struct_args, _mark_callback_base, _struct_key
from enum import Enum
from typing import Optional
import generated

from smoke.ParentInterface import ParentInterface

@_mark_callback_base
class ChildClassFromInterface(generated.smoke_ChildClassFromInterface):
    @classmethod
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        _install_callback_adapters(cls, __class__, [
            ("child_class_method", "__gluecodium_callback_736d6f6b652e4368696c64436c61737346726f6d496e746572666163652e6368696c64436c6173734d6574686f64", "method", None,
             lambda: ([], None)),
            ("root_method", "__gluecodium_callback_736d6f6b652e506172656e74496e746572666163652e726f6f744d6574686f64", "method", None,
             lambda: ([], None)),
            ("root_property", "__gluecodium_callback_736d6f6b652e506172656e74496e746572666163652e726f6f7450726f7065727479_get", "get", "get_root_property",
             lambda: ([], str)),
            ("root_property", "__gluecodium_callback_736d6f6b652e506172656e74496e746572666163652e726f6f7450726f7065727479_set", "set", "set_root_property",
             lambda: ([str], None)),
        ])
    def __init__(self, native=None):
        # Subclass the native pybind11 type so a Python override of an inherited virtual
        # method (from a parent interface or open base class) is dispatched through the
        # generated trampoline. When `native` is an existing native instance (returned by
        # a factory), adopt it via the generated adoption constructor and retain the original
        # native object for calls back into C++; otherwise construct a fresh trampoline.
        if native is not None and isinstance(native, generated.smoke_ChildClassFromInterface):
            super().__init__(native)
            self._native = native
        else:
            super().__init__()
            self._native = self

    def child_class_method(self):
        return _wrap(generated.smoke_ChildClassFromInterface.child_class_method(self), None)

    def root_method(self):
        return _wrap(generated.smoke_ChildClassFromInterface.root_method(self), None)

    @property
    def root_property(self) -> str:
        return _wrap(generated.smoke_ChildClassFromInterface.root_property.fget(self), str)

    @root_property.setter
    def root_property(self, value: str):
        generated.smoke_ChildClassFromInterface.root_property.fset(self, _unwrap(value, str))
