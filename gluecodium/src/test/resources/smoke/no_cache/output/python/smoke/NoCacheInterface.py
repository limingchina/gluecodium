

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase, _install_callback_adapters, _unwrap_struct_args, _mark_callback_base, _struct_key
from enum import Enum
from typing import Optional
import generated


@_mark_callback_base
class NoCacheInterface(generated.smoke_NoCacheInterface):
    @classmethod
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        _install_callback_adapters(cls, __class__, [
            ("foo", "__gluecodium_callback_736d6f6b652e4e6f4361636865496e746572666163652e666f6f", "method", None,
             lambda: ([], None)),
        ])
    def __init__(self, native=None):
        # Subclass the native pybind11 type so that a Python override of an interface
        # method is dispatched through the generated trampoline. When `native` is an
        # existing native instance (returned by a factory), adopt it via the generated
        # adoption constructor and retain the original native object for calls back into
        # C++; otherwise construct a fresh trampoline.
        if native is not None and isinstance(native, generated.smoke_NoCacheInterface):
            super().__init__(native)
            self._native = native
        else:
            super().__init__()
            self._native = self

    def foo(self):
        return _wrap(generated.smoke_NoCacheInterface.foo(self), None)
