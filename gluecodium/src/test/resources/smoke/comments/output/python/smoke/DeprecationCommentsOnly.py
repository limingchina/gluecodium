

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase, _install_callback_adapters, _unwrap_struct_args, _mark_callback_base, _struct_key
from enum import Enum
from typing import Optional
import generated


@_mark_callback_base
class DeprecationCommentsOnly(generated.smoke_DeprecationCommentsOnly):
    """"""
    @classmethod
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        _install_callback_adapters(cls, __class__, [
            ("some_method_with_all_comments", "__gluecodium_callback_736d6f6b652e4465707265636174696f6e436f6d6d656e74734f6e6c792e736f6d654d6574686f6457697468416c6c436f6d6d656e7473", "method", None,
             lambda: ([str], bool)),
            ("is_some_property", "__gluecodium_callback_736d6f6b652e4465707265636174696f6e436f6d6d656e74734f6e6c792e536f6d6550726f7065727479_get", "get", "is_some_property",
             lambda: ([], bool)),
            ("is_some_property", "__gluecodium_callback_736d6f6b652e4465707265636174696f6e436f6d6d656e74734f6e6c792e536f6d6550726f7065727479_set", "set", "set_some_property",
             lambda: ([bool], None)),
        ])
    def __init__(self, native=None):
        # Subclass the native pybind11 type so that a Python override of an interface
        # method is dispatched through the generated trampoline. When `native` is an
        # existing native instance (returned by a factory), adopt it via the generated
        # adoption constructor and retain the original native object for calls back into
        # C++; otherwise construct a fresh trampoline.
        if native is not None and isinstance(native, generated.smoke_DeprecationCommentsOnly):
            super().__init__(native)
            self._native = native
        else:
            super().__init__()
            self._native = self

    def some_method_with_all_comments(self, input: str) -> bool:
        """"""
        return _wrap(generated.smoke_DeprecationCommentsOnly.some_method_with_all_comments(self, _unwrap(input, str)), bool)

    @property
    def is_some_property(self) -> bool:
        """"""
        return _wrap(generated.smoke_DeprecationCommentsOnly.is_some_property.fget(self), bool)

    @is_some_property.setter
    def is_some_property(self, value: bool):
        generated.smoke_DeprecationCommentsOnly.is_some_property.fset(self, _unwrap(value, bool))

    class SomeStruct(_NativeBase):
        """"""
        def __init__(self, *args, **kwargs):
            if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_DeprecationCommentsOnly.SomeStruct):
                super().__init__(args[0])
            else:
                super().__init__(generated.smoke_DeprecationCommentsOnly.SomeStruct(
                    *[_unwrap(arg) for arg in args],
                    **{k: _unwrap(v) for k, v in kwargs.items()}
                ))

        @property
        def some_field(self) -> bool:
            """"""
            return _wrap(self._native.some_field, bool)
        @some_field.setter
        def some_field(self, value: bool):
          self._native.some_field = _unwrap(value, bool)




    class SomeEnum(Enum):
        """"""

        USELESS = generated.smoke_DeprecationCommentsOnly.SomeEnum.USELESS

        @property
        def _native(self):
            return self.value



    #:
    Usefulness = bool



    #:
    VERY_USEFUL = True
