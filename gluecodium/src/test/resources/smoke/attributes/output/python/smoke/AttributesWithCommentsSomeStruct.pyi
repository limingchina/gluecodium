

import typing


from _native_base import _NativeBase

import generated


class AttributesWithCommentsSomeStruct(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.AttributesWithCommentsSomeStruct):
            super().__init__(args[0])
        else:
            super().__init__(generated.AttributesWithCommentsSomeStruct(*[getattr(arg, "_native", arg) for arg in args]))

    Field comment
    @property
    def field(self) -> str:
        """Field comment"""
        return self._native.field
    @field.setter
    def field(self, value: str):
      self._native.field = getattr(value, "_native", value)


