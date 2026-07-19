

from __future__ import annotations



from _native_base import _NativeBase

import generated


class PublicStructWithInternalConstructors(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.PublicStructWithInternalConstructors):
            super().__init__(args[0])
        else:
            super().__init__(generated.PublicStructWithInternalConstructors(*[getattr(arg, "_native", arg) for arg in args]))


    @property
    def some_var(self) -> int:
        """"""
        return self._native.some_var
    @some_var.setter
    def some_var(self, value: int):
      self._native.some_var = getattr(value, "_native", value)


    @staticmethod
    def make() -> PublicStructWithInternalConstructors:
        """"""
        native_result = generated.PublicStructWithInternalConstructors.make()
        return PublicStructWithInternalConstructors(native_result)

