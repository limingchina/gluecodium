

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase, _install_callback_adapters, _unwrap_struct_args, _mark_callback_base, _struct_key
from enum import Enum
from typing import Optional
import generated

from smoke.ChildInterface import ChildInterface

@_mark_callback_base
class GrandChildInterface(generated.smoke_GrandChildInterface):
    @classmethod
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        _install_callback_adapters(cls, __class__, [
            ("grand_child_method", "__gluecodium_callback_736d6f6b652e4772616e644368696c64496e746572666163652e6772616e644368696c644d6574686f64", "method", None,
             lambda: ([], None)),
            ("child_method", "__gluecodium_callback_736d6f6b652e4368696c64496e746572666163652e6368696c644d6574686f64", "method", None,
             lambda: ([], None)),
            ("root_method", "__gluecodium_callback_736d6f6b652e506172656e74496e746572666163652e726f6f744d6574686f64", "method", None,
             lambda: ([], None)),
            ("root_property", "__gluecodium_callback_736d6f6b652e506172656e74496e746572666163652e726f6f7450726f7065727479_get", "get", "get_root_property",
             lambda: ([], str)),
            ("root_property", "__gluecodium_callback_736d6f6b652e506172656e74496e746572666163652e726f6f7450726f7065727479_set", "set", "set_root_property",
             lambda: ([str], None)),
        ])
    def __init__(self, native=None):
        # Subclass the native pybind11 type so that a Python override of an interface
        # method is dispatched through the generated trampoline. When `native` is an
        # existing native instance (returned by a factory), adopt it via the generated
        # adoption constructor and retain the original native object for calls back into
        # C++; otherwise construct a fresh trampoline.
        if native is not None and isinstance(native, generated.smoke_GrandChildInterface):
            super().__init__(native)
            self._native = native
        else:
            super().__init__()
            self._native = self

    def grand_child_method(self):
        return _wrap(generated.smoke_GrandChildInterface.grand_child_method(self), None)
