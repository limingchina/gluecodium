

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase, _install_callback_adapters, _unwrap_struct_args, _mark_callback_base
from enum import Enum
from typing import Optional
import generated


@_mark_callback_base
class AttributesInterface(generated.smoke_AttributesInterface):
    @classmethod
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        _install_callback_adapters(cls, __class__, [
            ("very_fun", "__gluecodium_callback_736d6f6b652e41747472696275746573496e746572666163652e7665727946756e", "method", None,
             lambda: ([str], None)),
            ("prop", "__gluecodium_callback_736d6f6b652e41747472696275746573496e746572666163652e70726f70_get", "get", "get_prop",
             lambda: ([], str)),
            ("prop", "__gluecodium_callback_736d6f6b652e41747472696275746573496e746572666163652e70726f70_set", "set", "set_prop",
             lambda: ([str], None)),
        ])
    def __init__(self, native=None):
        # Subclass the native pybind11 type so that a Python override of an interface
        # method is dispatched through the generated trampoline. When `native` is an
        # existing native instance (returned by a factory), adopt it via the generated
        # adoption constructor and retain the original native object for calls back into
        # C++; otherwise construct a fresh trampoline.
        if native is not None and isinstance(native, generated.smoke_AttributesInterface):
            super().__init__(native)
            self._native = native
        else:
            super().__init__()
            self._native = self

    def very_fun(self, param: str):
        return _wrap(generated.smoke_AttributesInterface.very_fun(self, _unwrap(param, str)), None)

    @property
    def prop(self) -> str:
        return _wrap(generated.smoke_AttributesInterface.prop.fget(self), str)

    @prop.setter
    def prop(self, value: str):
        generated.smoke_AttributesInterface.prop.fset(self, _unwrap(value, str))


    PI = False

