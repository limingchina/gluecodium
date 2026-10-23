

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase, _install_callback_adapters, _unwrap_struct_args, _mark_callback_base, _struct_key
from enum import Enum
from typing import Optional
import generated

from smoke.ParentInterfaceWithBool import ParentInterfaceWithBool

@_mark_callback_base
class ChildClassWithBool(generated.smoke_ChildClassWithBool):
    @classmethod
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        _install_callback_adapters(cls, __class__, [
            ("root_method", "__gluecodium_callback_736d6f6b652e506172656e74496e7465726661636557697468426f6f6c2e726f6f744d6574686f64", "method", None,
             lambda: ([bool], None)),
        ])
    def __init__(self, native=None):
        # Subclass the native pybind11 type so a Python override of an inherited virtual
        # method (from a parent interface or open base class) is dispatched through the
        # generated trampoline. When `native` is an existing native instance (returned by
        # a factory), adopt it via the generated adoption constructor and retain the original
        # native object for calls back into C++; otherwise construct a fresh trampoline.
        if native is not None and isinstance(native, generated.smoke_ChildClassWithBool):
            super().__init__(native)
            self._native = native
        else:
            super().__init__()
            self._native = self

    def root_method(self, input1: bool):
        return _wrap(generated.smoke_ChildClassWithBool.root_method(self, _unwrap(input1, bool)), None)
