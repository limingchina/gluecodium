

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase, _install_callback_adapters, _unwrap_struct_args, _mark_callback_base, _struct_key
from enum import Enum
from typing import Optional
import generated


@_mark_callback_base
class ParentClass(generated.smoke_ParentClass):
    @classmethod
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        _install_callback_adapters(cls, __class__, [
            ("parent_function", "__gluecodium_callback_736d6f6b652e506172656e74436c6173732e706172656e7446756e6374696f6e", "method", None,
             lambda: ([], None)),
            ("parent_property", "__gluecodium_callback_736d6f6b652e506172656e74436c6173732e706172656e7450726f7065727479_get", "get", "get_parent_property",
             lambda: ([], str)),
            ("parent_property", "__gluecodium_callback_736d6f6b652e506172656e74436c6173732e706172656e7450726f7065727479_set", "set", "set_parent_property",
             lambda: ([str], None)),
        ])
    def __init__(self, native=None):
        # Subclass the native pybind11 type so a Python override of an inherited virtual
        # method (from a parent interface or open base class) is dispatched through the
        # generated trampoline. When `native` is an existing native instance (returned by
        # a factory), adopt it via the generated adoption constructor and retain the original
        # native object for calls back into C++; otherwise construct a fresh trampoline.
        if native is not None and isinstance(native, generated.smoke_ParentClass):
            super().__init__(native)
            self._native = native
        else:
            super().__init__()
            self._native = self

    def parent_function(self):
        return _wrap(generated.smoke_ParentClass.parent_function(self), None)

    @property
    def parent_property(self) -> str:
        return _wrap(generated.smoke_ParentClass.parent_property.fget(self), str)

    @parent_property.setter
    def parent_property(self, value: str):
        generated.smoke_ParentClass.parent_property.fset(self, _unwrap(value, str))
