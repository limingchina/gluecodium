

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional



from _native_base import _NativeBase

import generated


class CommentsInterfaceSomeStruct(_NativeBase):
    """This is some very useful struct."""

    def __init__(self, *args, **kwargs):
        if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_CommentsInterfaceSomeStruct):
            super().__init__(args[0])
        else:
            super().__init__(generated.smoke_CommentsInterfaceSomeStruct(
                *[_unwrap(arg) for arg in args],
                **{k: _unwrap(v) for k, v in kwargs.items()}
            ))

    How useful this struct is
    @property
    def some_field(self) -> bool:
        """How useful this struct is"""
        return _wrap(self._native.some_field, bool)
    @some_field.setter
    def some_field(self, value: bool):
      self._native.some_field = _unwrap(value, bool)


