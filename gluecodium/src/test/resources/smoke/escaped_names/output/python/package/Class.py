

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase, _install_callback_adapters, _unwrap_struct_args, _mark_callback_base
from enum import Enum
from typing import Optional
import generated

from package.Interface import Interface
from package.Types import Types

@_mark_callback_base
class Class(generated.package_Class):
    @classmethod
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        _install_callback_adapters(cls, __class__, [
            ("fun", "__gluecodium_callback_7061636b6167652e636c6173732e66756e", "method", None,
             lambda: ([list[Types.Struct]], Types.Struct)),
            ("property", "__gluecodium_callback_7061636b6167652e636c6173732e70726f7065727479_get", "get", "get_property",
             lambda: ([], Types.Enum)),
            ("property", "__gluecodium_callback_7061636b6167652e636c6173732e70726f7065727479_set", "set", "set_property",
             lambda: ([Types.Enum], None)),
        ])
    def __init__(self, native=None):
        # Subclass the native pybind11 type so a Python override of an inherited virtual
        # method (from a parent interface or open base class) is dispatched through the
        # generated trampoline. When `native` is an existing native instance (returned by
        # a factory), adopt it via the generated adoption constructor and retain the original
        # native object for calls back into C++; otherwise construct a fresh trampoline.
        if native is not None and isinstance(native, generated.package_Class):
            super().__init__(native)
            self._native = native
        else:
            super().__init__()
            self._native = self

    @staticmethod
    def constructor() -> Class:
        native_result = generated.package_Class.constructor()
        return _get_or_create_wrapper(native_result, Class)

    def fun(self, double: list[Types.Struct]) -> Types.Struct:
        return _wrap(generated.package_Class.fun(self, _unwrap(double, list[Types.Struct])), Types.Struct)

    @property
    def property(self) -> Types.Enum:
        return _wrap(generated.package_Class.property.fget(self), Types.Enum)

    @property.setter
    def property(self, value: Types.Enum):
        generated.package_Class.property.fset(self, _unwrap(value, Types.Enum))


