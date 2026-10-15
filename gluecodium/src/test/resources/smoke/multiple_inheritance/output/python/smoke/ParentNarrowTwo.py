

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase, _install_callback_adapters, _unwrap_struct_args, _mark_callback_base, _struct_key
from enum import Enum
from typing import Optional
import generated


@_mark_callback_base
class ParentNarrowTwo(generated.smoke_ParentNarrowTwo):
    @classmethod
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        _install_callback_adapters(cls, __class__, [
            ("parent_function_two", "__gluecodium_callback_736d6f6b652e506172656e744e6172726f7754776f2e706172656e7446756e6374696f6e54776f", "method", None,
             lambda: ([], None)),
            ("parent_property_two", "__gluecodium_callback_736d6f6b652e506172656e744e6172726f7754776f2e706172656e7450726f706572747954776f_get", "get", "get_parent_property_two",
             lambda: ([], str)),
            ("parent_property_two", "__gluecodium_callback_736d6f6b652e506172656e744e6172726f7754776f2e706172656e7450726f706572747954776f_set", "set", "set_parent_property_two",
             lambda: ([str], None)),
        ])
    def __init__(self, native=None):
        # Subclass the native pybind11 type so that a Python override of an interface
        # method is dispatched through the generated trampoline. When `native` is an
        # existing native instance (returned by a factory), adopt it via the generated
        # adoption constructor and retain the original native object for calls back into
        # C++; otherwise construct a fresh trampoline.
        if native is not None and isinstance(native, generated.smoke_ParentNarrowTwo):
            super().__init__(native)
            # Narrow interfaces cross back into C++ through the forwarding trampoline,
            # preserving only this interface's type and not the original object's identity.
            self._native = self
        else:
            super().__init__()
            self._native = self

    def parent_function_two(self):
        return _wrap(generated.smoke_ParentNarrowTwo.parent_function_two(self), None)

    @property
    def parent_property_two(self) -> str:
        return _wrap(generated.smoke_ParentNarrowTwo.parent_property_two.fget(self), str)

    @parent_property_two.setter
    def parent_property_two(self, value: str):
        generated.smoke_ParentNarrowTwo.parent_property_two.fset(self, _unwrap(value, str))
