

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase, _install_callback_adapters, _unwrap_struct_args, _mark_callback_base, _struct_key
from enum import Enum
from typing import Optional
import generated


class ExternalEquatable(_NativeBase):
    def __init__(self, *args, **kwargs):
        if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_ExternalEquatable):
            super().__init__(args[0])
        else:
            super().__init__(generated.smoke_ExternalEquatable(
                *[_unwrap(arg) for arg in args],
                **{k: _unwrap(v) for k, v in kwargs.items()}
            ))

    class ExternalEquatableStruct(_NativeBase):
        def __init__(self, *args, **kwargs):
            if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_ExternalEquatable.ExternalEquatableStruct):
                super().__init__(args[0])
            else:
                super().__init__(generated.smoke_ExternalEquatable.ExternalEquatableStruct(
                    *[_unwrap(arg) for arg in args],
                    **{k: _unwrap(v) for k, v in kwargs.items()}
                ))

        def __eq__(self, other: object) -> bool:
            if not isinstance(other, __class__):
                return False
            return self._native.__gluecodium_equals__(other._native)

        __hash__ = None

        def as_key(self):
            """Return an isolated immutable value snapshot for dictionaries and sets."""
            return _struct_key(self, __class__)

        @property
        def foo_field(self) -> str:
            return _wrap(self._native.foo_field, str)
        @foo_field.setter
        def foo_field(self, value: str):
          self._native.foo_field = _unwrap(value, str)
