

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase, _install_callback_adapters, _unwrap_struct_args, _mark_callback_base, _struct_key
from enum import Enum
from typing import Optional
import generated


@_mark_callback_base
class InterfaceWithStatic(generated.smoke_InterfaceWithStatic):
    @classmethod
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        _install_callback_adapters(cls, __class__, [
            ("regular_function", "__gluecodium_callback_736d6f6b652e496e74657266616365576974685374617469632e726567756c617246756e6374696f6e", "method", None,
             lambda: ([], str)),
            ("regular_property", "__gluecodium_callback_736d6f6b652e496e74657266616365576974685374617469632e726567756c617250726f7065727479_get", "get", "get_regular_property",
             lambda: ([], str)),
            ("regular_property", "__gluecodium_callback_736d6f6b652e496e74657266616365576974685374617469632e726567756c617250726f7065727479_set", "set", "set_regular_property",
             lambda: ([str], None)),
        ])
    def __init__(self, native=None):
        # Subclass the native pybind11 type so that a Python override of an interface
        # method is dispatched through the generated trampoline. When `native` is an
        # existing native instance (returned by a factory), adopt it via the generated
        # adoption constructor and retain the original native object for calls back into
        # C++; otherwise construct a fresh trampoline.
        if native is not None and isinstance(native, generated.smoke_InterfaceWithStatic):
            super().__init__(native)
            self._native = native
        else:
            super().__init__()
            self._native = self

    def regular_function(self) -> str:
        return _wrap(generated.smoke_InterfaceWithStatic.regular_function(self), str)

    @staticmethod
    def static_function() -> str:
        return _wrap(generated.smoke_InterfaceWithStatic.static_function(), str)

    @property
    def regular_property(self) -> str:
        return _wrap(generated.smoke_InterfaceWithStatic.regular_property.fget(self), str)

    @regular_property.setter
    def regular_property(self, value: str):
        generated.smoke_InterfaceWithStatic.regular_property.fset(self, _unwrap(value, str))

    @staticmethod
    def static_property() -> str:
        return _wrap(generated.smoke_InterfaceWithStatic.static_property(), str)

    @staticmethod
    def static_property_set(value: str):
        generated.smoke_InterfaceWithStatic.static_property_set(_unwrap(value, str))
