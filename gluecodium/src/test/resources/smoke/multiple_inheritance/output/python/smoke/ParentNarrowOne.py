

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase, _install_callback_adapters, _unwrap_struct_args, _mark_callback_base, _struct_key
from enum import Enum
from typing import Optional
import generated


@_mark_callback_base
class ParentNarrowOne(generated.smoke_ParentNarrowOne):
    @classmethod
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        _install_callback_adapters(cls, __class__, [
            ("parent_function_one", "__gluecodium_callback_736d6f6b652e506172656e744e6172726f774f6e652e706172656e7446756e6374696f6e4f6e65", "method", None,
             lambda: ([], None)),
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
        if native is not None and isinstance(native, generated.smoke_ParentNarrowOne):
            super().__init__(native)
            # Narrow interfaces cross back into C++ through the forwarding trampoline,
            # preserving only this interface's type and not the original object's identity.
            self._native = self
        else:
            super().__init__()
            self._native = self

    def parent_function_one(self):
        return _wrap(generated.smoke_ParentNarrowOne.parent_function_one(self), None)

    @property
    def parent_property_one(self) -> str:
        return _wrap(generated.smoke_ParentNarrowOne.parent_property_one.fget(self), str)

    @parent_property_one.setter
    def parent_property_one(self, value: str):
        generated.smoke_ParentNarrowOne.parent_property_one.fset(self, _unwrap(value, str))
