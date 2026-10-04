

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase, _install_callback_adapters, _unwrap_struct_args, _mark_callback_base
from enum import Enum
from typing import Optional
import generated

from another.SomeCoolClassType import SomeCoolClassType

@_mark_callback_base
class ParentInterface(generated.smoke_ParentInterface):
    @classmethod
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        _install_callback_adapters(cls, __class__, [
            ("parent_function", "__gluecodium_callback_736d6f6b652e506172656e74496e746572666163652e706172656e7446756e6374696f6e", "method", None,
             lambda: ([], None)),
            ("some_function_that_uses_type_from_another_package", "__gluecodium_callback_736d6f6b652e506172656e74496e746572666163652e736f6d655f66756e6374696f6e5f746861745f757365735f747970655f66726f6d5f616e6f746865725f7061636b616765", "method", None,
             lambda: ([SomeCoolClassType], None)),
            ("parent_property", "__gluecodium_callback_736d6f6b652e506172656e74496e746572666163652e706172656e7450726f7065727479_get", "get", "get_parent_property",
             lambda: ([], str)),
            ("parent_property", "__gluecodium_callback_736d6f6b652e506172656e74496e746572666163652e706172656e7450726f7065727479_set", "set", "set_parent_property",
             lambda: ([str], None)),
        ])
    def __init__(self, native=None):
        # Subclass the native pybind11 type so that a Python override of an interface
        # method is dispatched through the generated trampoline. When `native` is an
        # existing native instance (returned by a factory), adopt it via the generated
        # adoption constructor and retain the original native object for calls back into
        # C++; otherwise construct a fresh trampoline.
        if native is not None and isinstance(native, generated.smoke_ParentInterface):
            super().__init__(native)
            self._native = native
        else:
            super().__init__()
            self._native = self

    def parent_function(self):
        return _wrap(generated.smoke_ParentInterface.parent_function(self), None)

    def some_function_that_uses_type_from_another_package(self, some_param: SomeCoolClassType):
        return _wrap(generated.smoke_ParentInterface.some_function_that_uses_type_from_another_package(self, _unwrap(some_param, SomeCoolClassType)), None)

    @property
    def parent_property(self) -> str:
        return _wrap(generated.smoke_ParentInterface.parent_property.fget(self), str)

    @parent_property.setter
    def parent_property(self, value: str):
        generated.smoke_ParentInterface.parent_property.fset(self, _unwrap(value, str))


