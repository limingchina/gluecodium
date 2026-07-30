

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper
from typing import Optional



from _native_base import _NativeBase

import generated


class commentsSomeStruct(_NativeBase):
    """This is some very useful struct."""
    def __init__(self, *args, **kwargs):
        if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_commentsSomeStruct):
            super().__init__(args[0])
        else:
            super().__init__(generated.smoke_commentsSomeStruct(
                *[_unwrap(arg) for arg in args],
                **{k: _unwrap(v) for k, v in kwargs.items()}
            ))

    @property
    def some_field(self) -> bool:
        """How useful this struct is
remains to be seen"""
        return _wrap(self._native.some_field, bool)
    @some_field.setter
    def some_field(self, value: bool):
      self._native.some_field = _unwrap(value, bool)


    @property
    def nullable_field(self):
        """Can be `None`"""
        return _wrap(self._native.nullable_field, Optional[str])
    @nullable_field.setter
    def nullable_field(self, value):
      self._native.nullable_field = _unwrap(value, Optional[str])


    def some_struct_method(self):
        """This is some struct method that does nothing."""
        return _wrap(self._native.some_struct_method(), None)

    @staticmethod
    def some_static_struct_method():
        """This is some static struct method that does nothing."""
        generated.smoke_commentsSomeStruct.some_static_struct_method()

