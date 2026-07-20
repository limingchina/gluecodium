

from __future__ import annotations



from _native_base import _NativeBase

import generated


class ExcludedCommentsSomeStruct(_NativeBase):
    """This is some very useful struct."""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.ExcludedCommentsSomeStruct):
            super().__init__(args[0])
        else:
            super().__init__(generated.ExcludedCommentsSomeStruct(*[getattr(arg, "_native", arg) for arg in args]))

    How useful this struct is
    remains to be seen
    @property
    def some_field(self) -> bool:
        """How useful this struct is
remains to be seen"""
        return self._native.some_field
    @some_field.setter
    def some_field(self, value: bool):
      self._native.some_field = getattr(value, "_native", value)


