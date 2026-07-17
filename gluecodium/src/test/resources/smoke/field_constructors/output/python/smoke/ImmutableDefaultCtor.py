

from __future__ import annotations



from _native_base import _NativeBase

import generated


class ImmutableDefaultCtor(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.ImmutableDefaultCtor):
            super().__init__(args[0])
        else:
            super().__init__(generated.ImmutableDefaultCtor(*[getattr(arg, "_native", arg) for arg in args]))


    @property
    def string_field(self) -> str:
        """"""
        return self._native.string_field
    @string_field.setter
    def string_field(self, value: str):
      self._native.string_field = getattr(value, "_native", value)


