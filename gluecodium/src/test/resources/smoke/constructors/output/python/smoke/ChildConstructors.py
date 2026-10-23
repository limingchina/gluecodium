

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase, _install_callback_adapters, _unwrap_struct_args, _mark_callback_base, _struct_key
from enum import Enum
from typing import Optional
import generated

from smoke.Constructors import Constructors

@_mark_callback_base
class ChildConstructors(generated.smoke_ChildConstructors):
    @classmethod
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        _install_callback_adapters(cls, __class__, [
        ])
    def __init__(self, native=None):
        # Subclass the native pybind11 type so a Python override of an inherited virtual
        # method (from a parent interface or open base class) is dispatched through the
        # generated trampoline. When `native` is an existing native instance (returned by
        # a factory), adopt it via the generated adoption constructor and retain the original
        # native object for calls back into C++; otherwise construct a fresh trampoline.
        if native is not None and isinstance(native, generated.smoke_ChildConstructors):
            super().__init__(native)
            self._native = native
        else:
            super().__init__()
            self._native = self

    @staticmethod
    def create(*args, **kwargs) -> ChildConstructors:
        native_result = generated.smoke_ChildConstructors.create(*[_unwrap(a) for a in args], **{k: _unwrap(v) for k, v in kwargs.items()})
        return _get_or_create_wrapper(native_result, ChildConstructors)
