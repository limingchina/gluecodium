

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase, _install_callback_adapters, _unwrap_struct_args, _mark_callback_base, _struct_key
from enum import Enum
from typing import Optional
import generated

from smoke.ParentClass import ParentClass
from smoke.ParentNarrowOne import ParentNarrowOne

@_mark_callback_base
class FirstParentIsClassClass(generated.smoke_FirstParentIsClassClass):
    @classmethod
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        _install_callback_adapters(cls, __class__, [
            ("child_function", "__gluecodium_callback_736d6f6b652e4669727374506172656e744973436c617373436c6173732e6368696c6446756e6374696f6e", "method", None,
             lambda: ([], None)),
            ("parent_function", "__gluecodium_callback_736d6f6b652e506172656e74436c6173732e706172656e7446756e6374696f6e", "method", None,
             lambda: ([], None)),
            ("parent_function_one", "__gluecodium_callback_736d6f6b652e506172656e744e6172726f774f6e652e706172656e7446756e6374696f6e4f6e65", "method", None,
             lambda: ([], None)),
            ("child_property", "__gluecodium_callback_736d6f6b652e4669727374506172656e744973436c617373436c6173732e6368696c6450726f7065727479_get", "get", "get_child_property",
             lambda: ([], str)),
            ("child_property", "__gluecodium_callback_736d6f6b652e4669727374506172656e744973436c617373436c6173732e6368696c6450726f7065727479_set", "set", "set_child_property",
             lambda: ([str], None)),
            ("parent_property", "__gluecodium_callback_736d6f6b652e506172656e74436c6173732e706172656e7450726f7065727479_get", "get", "get_parent_property",
             lambda: ([], str)),
            ("parent_property", "__gluecodium_callback_736d6f6b652e506172656e74436c6173732e706172656e7450726f7065727479_set", "set", "set_parent_property",
             lambda: ([str], None)),
            ("parent_property_one", "__gluecodium_callback_736d6f6b652e506172656e744e6172726f774f6e652e706172656e7450726f70657274794f6e65_get", "get", "get_parent_property_one",
             lambda: ([], str)),
            ("parent_property_one", "__gluecodium_callback_736d6f6b652e506172656e744e6172726f774f6e652e706172656e7450726f70657274794f6e65_set", "set", "set_parent_property_one",
             lambda: ([str], None)),
        ])
    def __init__(self, native=None):
        # Subclass the native pybind11 type so a Python override of an inherited virtual
        # method (from a parent interface or open base class) is dispatched through the
        # generated trampoline. When `native` is an existing native instance (returned by
        # a factory), adopt it via the generated adoption constructor and retain the original
        # native object for calls back into C++; otherwise construct a fresh trampoline.
        if native is not None and isinstance(native, generated.smoke_FirstParentIsClassClass):
            super().__init__(native)
            self._native = native
        else:
            super().__init__()
            self._native = self

    def child_function(self):
        return _wrap(generated.smoke_FirstParentIsClassClass.child_function(self), None)

    def parent_function_one(self):
        return _wrap(generated.smoke_FirstParentIsClassClass.parent_function_one(self), None)

    @property
    def child_property(self) -> str:
        return _wrap(generated.smoke_FirstParentIsClassClass.child_property.fget(self), str)

    @child_property.setter
    def child_property(self, value: str):
        generated.smoke_FirstParentIsClassClass.child_property.fset(self, _unwrap(value, str))

    @property
    def parent_property_one(self) -> str:
        return _wrap(generated.smoke_FirstParentIsClassClass.parent_property_one.fget(self), str)

    @parent_property_one.setter
    def parent_property_one(self, value: str):
        generated.smoke_FirstParentIsClassClass.parent_property_one.fset(self, _unwrap(value, str))
