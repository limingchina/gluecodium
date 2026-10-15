

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase, _install_callback_adapters, _unwrap_struct_args, _mark_callback_base, _struct_key
from enum import Enum
from typing import Optional
import generated


@_mark_callback_base
class InterfaceWithOverloads(generated.smoke_InterfaceWithOverloads):
    @classmethod
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        _install_callback_adapters(cls, __class__, [
            ("parent_method", "__gluecodium_callback_736d6f6b652e496e74657266616365576974684f7665726c6f6164732e706172656e744d6574686f64", "method", None,
             lambda: ([], None)),
            ("parent_method", "__gluecodium_callback_736d6f6b652e496e74657266616365576974684f7665726c6f6164732e706172656e744d6574686f643a31", "method", None,
             lambda: ([str], None)),
        ])
    def __init__(self, native=None):
        # Subclass the native pybind11 type so that a Python override of an interface
        # method is dispatched through the generated trampoline. When `native` is an
        # existing native instance (returned by a factory), adopt it via the generated
        # adoption constructor and retain the original native object for calls back into
        # C++; otherwise construct a fresh trampoline.
        if native is not None and isinstance(native, generated.smoke_InterfaceWithOverloads):
            super().__init__(native)
            self._native = native
        else:
            super().__init__()
            self._native = self

    def parent_method(self, *args, **kwargs):
        return _wrap(generated.smoke_InterfaceWithOverloads.parent_method(self, *[_unwrap(a) for a in args], **{k: _unwrap(v) for k, v in kwargs.items()}), None)
