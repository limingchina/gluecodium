

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase, _install_callback_adapters, _unwrap_struct_args, _mark_callback_base, _struct_key
from enum import Enum
from typing import Optional
import generated

from smoke.ParentClass import ParentClass

@_mark_callback_base
class OuterClassWithInheritance(generated.smoke_OuterClassWithInheritance):
    @classmethod
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        _install_callback_adapters(cls, __class__, [
            ("foo", "__gluecodium_callback_736d6f6b652e4f75746572436c61737357697468496e6865726974616e63652e666f6f", "method", None,
             lambda: ([str], str)),
            ("parent_fun", "__gluecodium_callback_736d6f6b652e506172656e74436c6173732e706172656e7446756e", "method", None,
             lambda: ([], None)),
            ("parent_property", "__gluecodium_callback_736d6f6b652e506172656e74436c6173732e706172656e7450726f7065727479_get", "get", "get_parent_property",
             lambda: ([], str)),
            ("parent_property", "__gluecodium_callback_736d6f6b652e506172656e74436c6173732e706172656e7450726f7065727479_set", "set", "set_parent_property",
             lambda: ([str], None)),
        ])
    def __init__(self, native=None):
        # Subclass the native pybind11 type so a Python override of an inherited virtual
        # method (from a parent interface or open base class) is dispatched through the
        # generated trampoline. When `native` is an existing native instance (returned by
        # a factory), adopt it via the generated adoption constructor and retain the original
        # native object for calls back into C++; otherwise construct a fresh trampoline.
        if native is not None and isinstance(native, generated.smoke_OuterClassWithInheritance):
            super().__init__(native)
            self._native = native
        else:
            super().__init__()
            self._native = self

    def foo(self, input: str) -> str:
        return _wrap(generated.smoke_OuterClassWithInheritance.foo(self, _unwrap(input, str)), str)

    class InnerClass(_NativeBase):
        def __init__(self, native):
            super().__init__(native)

        def bar(self, input: str) -> str:
            return _wrap(self._native.bar(_unwrap(input, str)), str)



    @_mark_callback_base
    class InnerInterface(generated.smoke_OuterClassWithInheritance.InnerInterface):
        @classmethod
        def __init_subclass__(cls, **kwargs):
            super().__init_subclass__(**kwargs)
            _install_callback_adapters(cls, __class__, [
                ("baz", "__gluecodium_callback_736d6f6b652e4f75746572436c61737357697468496e6865726974616e63652e496e6e6572496e746572666163652e62617a", "method", None,
                 lambda: ([str], str)),
            ])
        def __init__(self, native=None):
            # Subclass the native pybind11 type so that a Python override of an interface
            # method is dispatched through the generated trampoline. When `native` is an
            # existing native instance (returned by a factory), adopt it via the generated
            # adoption constructor and retain the original native object for calls back into
            # C++; otherwise construct a fresh trampoline.
            if native is not None and isinstance(native, generated.smoke_OuterClassWithInheritance.InnerInterface):
                super().__init__(native)
                self._native = native
            else:
                super().__init__()
                self._native = self

        def baz(self, input: str) -> str:
            return _wrap(generated.smoke_OuterClassWithInheritance.InnerInterface.baz(self, _unwrap(input, str)), str)
