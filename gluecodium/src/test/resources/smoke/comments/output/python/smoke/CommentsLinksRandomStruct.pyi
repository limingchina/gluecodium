

from smoke.commentsSomeStruct import commentsSomeStruct
import typing


from _native_base import _NativeBase

import generated


class CommentsLinksRandomStruct(_NativeBase):
    """Links also work in:"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.CommentsLinksRandomStruct):
            super().__init__(args[0])
        else:
            super().__init__(generated.CommentsLinksRandomStruct(*[_unwrap(arg) for arg in args]))

    Some random field [comments.SomeStruct]
    @property
    def random_field(self) -> commentsSomeStruct:
        """Some random field [comments.SomeStruct]"""
        return _wrap(self._native.random_field, commentsSomeStruct)
    @random_field.setter
    def random_field(self, value: commentsSomeStruct):
      self._native.random_field = _unwrap(value, commentsSomeStruct)


