

import typing


from _native_base import _NativeBase

import generated


class SkipTypesNotInSwift(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.SkipTypesNotInSwift):
            super().__init__(args[0])
        else:
            super().__init__(generated.SkipTypesNotInSwift(*[getattr(arg, "_native", arg) for arg in args]))


    @property
    def foo_field(self) -> str:
        """"""
        return self._native.foo_field
    @foo_field.setter
    def foo_field(self, value: str):
      self._native.foo_field = getattr(value, "_native", value)


