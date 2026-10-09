

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase, _install_callback_adapters, _unwrap_struct_args, _mark_callback_base, _struct_key
from enum import Enum
from typing import Optional
import generated


@_mark_callback_base
class PropertiesInterface(generated.smoke_PropertiesInterface):
    @classmethod
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        _install_callback_adapters(cls, __class__, [
            ("struct_property", "__gluecodium_callback_736d6f6b652e50726f70657274696573496e746572666163652e73747275637450726f7065727479_get", "get", "get_struct_property",
             lambda: ([], PropertiesInterface.ExampleStruct)),
            ("struct_property", "__gluecodium_callback_736d6f6b652e50726f70657274696573496e746572666163652e73747275637450726f7065727479_set", "set", "set_struct_property",
             lambda: ([PropertiesInterface.ExampleStruct], None)),
        ])
    def __init__(self, native=None):
        # Subclass the native pybind11 type so that a Python override of an interface
        # method is dispatched through the generated trampoline. When `native` is an
        # existing native instance (returned by a factory), adopt it via the generated
        # adoption constructor and retain the original native object for calls back into
        # C++; otherwise construct a fresh trampoline.
        if native is not None and isinstance(native, generated.smoke_PropertiesInterface):
            super().__init__(native)
            self._native = native
        else:
            super().__init__()
            self._native = self

    @property
    def struct_property(self) -> PropertiesInterface.ExampleStruct:
        return _wrap(generated.smoke_PropertiesInterface.struct_property.fget(self), PropertiesInterface.ExampleStruct)

    @struct_property.setter
    def struct_property(self, value: PropertiesInterface.ExampleStruct):
        generated.smoke_PropertiesInterface.struct_property.fset(self, _unwrap(value, PropertiesInterface.ExampleStruct))

    class ExampleStruct(_NativeBase):
        def __init__(self, *args, **kwargs):
            if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_PropertiesInterface.ExampleStruct):
                super().__init__(args[0])
            else:
                super().__init__(generated.smoke_PropertiesInterface.ExampleStruct(
                    *[_unwrap(arg) for arg in args],
                    **{k: _unwrap(v) for k, v in kwargs.items()}
                ))

        @property
        def value(self) -> float:
            return _wrap(self._native.value, float)
        @value.setter
        def value(self, value: float):
          self._native.value = _unwrap(value, float)
