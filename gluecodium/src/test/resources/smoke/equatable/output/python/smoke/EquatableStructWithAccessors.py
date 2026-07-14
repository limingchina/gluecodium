

from __future__ import annotations



from _native_base import _NativeBase

import generated


class EquatableStructWithAccessors(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], EquatableStructWithAccessors):
            super().__init__(args[0])
        else:
            super().__init__(generated.EquatableStructWithAccessors(*[getattr(arg, "_native", arg) for arg in args]))


    @property
    def foo_field(self) -> str:
        """"""
        return self._native.foo_field

    @foo_field.setter
    def foo_field(self, value: str):
      self._native.foo_field = getattr(value, "_native", value)


