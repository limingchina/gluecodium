

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase, _install_callback_adapters, _unwrap_struct_args, _mark_callback_base, _struct_key
from enum import Enum
from typing import Optional
import generated

from another.SomeCoolClassType import SomeCoolClassType
from smoke.ParentInterface import ParentInterface
from smoke.ParentNarrowOne import ParentNarrowOne

@_mark_callback_base
class FirstParentIsInterfaceInterface(generated.smoke_FirstParentIsInterfaceInterface):
    @classmethod
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        _install_callback_adapters(cls, __class__, [
            ("child_function", "__gluecodium_callback_736d6f6b652e4669727374506172656e744973496e74657266616365496e746572666163652e6368696c6446756e6374696f6e", "method", None,
             lambda: ([], None)),
            ("parent_function", "__gluecodium_callback_736d6f6b652e506172656e74496e746572666163652e706172656e7446756e6374696f6e", "method", None,
             lambda: ([], None)),
            ("some_function_that_uses_type_from_another_package", "__gluecodium_callback_736d6f6b652e506172656e74496e746572666163652e736f6d655f66756e6374696f6e5f746861745f757365735f747970655f66726f6d5f616e6f746865725f7061636b616765", "method", None,
             lambda: ([SomeCoolClassType], None)),
            ("parent_function_one", "__gluecodium_callback_736d6f6b652e506172656e744e6172726f774f6e652e706172656e7446756e6374696f6e4f6e65", "method", None,
             lambda: ([], None)),
            ("child_property", "__gluecodium_callback_736d6f6b652e4669727374506172656e744973496e74657266616365496e746572666163652e6368696c6450726f7065727479_get", "get", "get_child_property",
             lambda: ([], str)),
            ("child_property", "__gluecodium_callback_736d6f6b652e4669727374506172656e744973496e74657266616365496e746572666163652e6368696c6450726f7065727479_set", "set", "set_child_property",
             lambda: ([str], None)),
            ("parent_property", "__gluecodium_callback_736d6f6b652e506172656e74496e746572666163652e706172656e7450726f7065727479_get", "get", "get_parent_property",
             lambda: ([], str)),
            ("parent_property", "__gluecodium_callback_736d6f6b652e506172656e74496e746572666163652e706172656e7450726f7065727479_set", "set", "set_parent_property",
             lambda: ([str], None)),
            ("parent_property_one", "__gluecodium_callback_736d6f6b652e506172656e744e6172726f774f6e652e706172656e7450726f70657274794f6e65_get", "get", "get_parent_property_one",
             lambda: ([], str)),
            ("parent_property_one", "__gluecodium_callback_736d6f6b652e506172656e744e6172726f774f6e652e706172656e7450726f70657274794f6e65_set", "set", "set_parent_property_one",
             lambda: ([str], None)),
        ])
    def __init__(self, native=None):
        # Subclass the native pybind11 type so that a Python override of an interface
        # method is dispatched through the generated trampoline. When `native` is an
        # existing native instance (returned by a factory), adopt it via the generated
        # adoption constructor and retain the original native object for calls back into
        # C++; otherwise construct a fresh trampoline.
        if native is not None and isinstance(native, generated.smoke_FirstParentIsInterfaceInterface):
            super().__init__(native)
            self._native = native
        else:
            super().__init__()
            self._native = self

    def child_function(self):
        return _wrap(generated.smoke_FirstParentIsInterfaceInterface.child_function(self), None)

    @property
    def child_property(self) -> str:
        return _wrap(generated.smoke_FirstParentIsInterfaceInterface.child_property.fget(self), str)

    @child_property.setter
    def child_property(self, value: str):
        generated.smoke_FirstParentIsInterfaceInterface.child_property.fset(self, _unwrap(value, str))
