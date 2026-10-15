

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase, _install_callback_adapters, _unwrap_struct_args, _mark_callback_base, _struct_key
from enum import Enum
from typing import Optional
import generated

from smoke.ParentClass import ParentClass

@_mark_callback_base
class ForwardDeclarationBug(generated.smoke_ForwardDeclarationBug):
    @classmethod
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        _install_callback_adapters(cls, __class__, [
            ("foo", "__gluecodium_callback_736d6f6b652e466f72776172644465636c61726174696f6e4275672e666f6f", "method", None,
             lambda: ([ParentClass], None)),
            ("root_method", "__gluecodium_callback_736d6f6b652e506172656e74436c6173732e726f6f744d6574686f64", "method", None,
             lambda: ([], None)),
            ("root_property", "__gluecodium_callback_736d6f6b652e506172656e74436c6173732e726f6f7450726f7065727479_get", "get", "get_root_property",
             lambda: ([], str)),
            ("root_property", "__gluecodium_callback_736d6f6b652e506172656e74436c6173732e726f6f7450726f7065727479_set", "set", "set_root_property",
             lambda: ([str], None)),
        ])
    def __init__(self, native=None):
        # Subclass the native pybind11 type so a Python override of an inherited virtual
        # method (from a parent interface or open base class) is dispatched through the
        # generated trampoline. When `native` is an existing native instance (returned by
        # a factory), adopt it via the generated adoption constructor and retain the original
        # native object for calls back into C++; otherwise construct a fresh trampoline.
        if native is not None and isinstance(native, generated.smoke_ForwardDeclarationBug):
            super().__init__(native)
            self._native = native
        else:
            super().__init__()
            self._native = self

    def foo(self, bar: ParentClass):
        return _wrap(generated.smoke_ForwardDeclarationBug.foo(self, _unwrap(bar, ParentClass)), None)
