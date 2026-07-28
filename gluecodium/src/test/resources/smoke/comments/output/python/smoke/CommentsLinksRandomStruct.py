

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper
from typing import Optional

from smoke.commentsSomeStruct import commentsSomeStruct


from _native_base import _NativeBase

import generated


class CommentsLinksRandomStruct(_NativeBase):
    """Links also work in:"""

    def __init__(self, *args, **kwargs):
        if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_CommentsLinksRandomStruct):
            super().__init__(args[0])
        else:
            super().__init__(generated.smoke_CommentsLinksRandomStruct(
                *[_unwrap(arg) for arg in args],
                **{k: _unwrap(v) for k, v in kwargs.items()}
            ))

    Some random field [comments.SomeStruct]
    @property
    def random_field(self) -> commentsSomeStruct:
        """Some random field [comments.SomeStruct]"""
        return _wrap(self._native.random_field, commentsSomeStruct)
    @random_field.setter
    def random_field(self, value: commentsSomeStruct):
      self._native.random_field = _unwrap(value, commentsSomeStruct)


