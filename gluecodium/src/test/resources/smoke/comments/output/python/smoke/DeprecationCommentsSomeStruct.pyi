

import typing


from _native_base import _NativeBase

import generated


class DeprecationCommentsSomeStruct(_NativeBase):
    """This is some very useful struct."""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.DeprecationCommentsSomeStruct):
            super().__init__(args[0])
        else:
            super().__init__(generated.DeprecationCommentsSomeStruct(*[getattr(arg, "_native", arg) for arg in args]))

    How useful this struct is.
    @property
    def some_field(self) -> bool:
        """How useful this struct is."""
        return self._native.some_field
    @some_field.setter
    def some_field(self, value: bool):
      self._native.some_field = getattr(value, "_native", value)


