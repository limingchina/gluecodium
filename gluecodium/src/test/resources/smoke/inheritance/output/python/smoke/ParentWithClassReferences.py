

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase, _install_callback_adapters, _unwrap_struct_args, _mark_callback_base
from enum import Enum
from typing import Optional
import generated

from smoke.ChildClassFromClass import ChildClassFromClass
from smoke.ParentClass import ParentClass

@_mark_callback_base
class ParentWithClassReferences(generated.smoke_ParentWithClassReferences):
    @classmethod
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        _install_callback_adapters(cls, __class__, [
            ("class_function", "__gluecodium_callback_736d6f6b652e506172656e7457697468436c6173735265666572656e6365732e636c61737346756e6374696f6e", "method", None,
             lambda: ([], ChildClassFromClass)),
            ("class_property", "__gluecodium_callback_736d6f6b652e506172656e7457697468436c6173735265666572656e6365732e636c61737350726f7065727479_get", "get", "get_class_property",
             lambda: ([], ParentClass)),
            ("class_property", "__gluecodium_callback_736d6f6b652e506172656e7457697468436c6173735265666572656e6365732e636c61737350726f7065727479_set", "set", "set_class_property",
             lambda: ([ParentClass], None)),
        ])
    def __init__(self, native=None):
        # Subclass the native pybind11 type so that a Python override of an interface
        # method is dispatched through the generated trampoline. When `native` is an
        # existing native instance (returned by a factory), adopt it via the generated
        # adoption constructor and retain the original native object for calls back into
        # C++; otherwise construct a fresh trampoline.
        if native is not None and isinstance(native, generated.smoke_ParentWithClassReferences):
            super().__init__(native)
            self._native = native
        else:
            super().__init__()
            self._native = self

    def class_function(self) -> ChildClassFromClass:
        return _wrap(generated.smoke_ParentWithClassReferences.class_function(self), ChildClassFromClass)

    @property
    def class_property(self) -> ParentClass:
        return _wrap(generated.smoke_ParentWithClassReferences.class_property.fget(self), ParentClass)

    @class_property.setter
    def class_property(self, value: ParentClass):
        generated.smoke_ParentWithClassReferences.class_property.fset(self, _unwrap(value, ParentClass))


