

from __future__ import annotations



from _native_base import _NativeBase

import generated


class FieldConstructorsInternal(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and hasattr(args[0], "_native"):
            super().__init__(args[0]._native)
        else:
            super().__init__(generated.FieldConstructorsInternal(*[getattr(arg, "_native", arg) for arg in args]))


    @property
    def public_field(self) -> str:
        """"""
        return self._native.public_field
    @public_field.setter
    def public_field(self, value: str):
      self._native.public_field = getattr(value, "_native", value)



    @property
    def internal_field(self) -> float:
        """"""
        return self._native.internal_field
    @internal_field.setter
    def internal_field(self, value: float):
      self._native.internal_field = getattr(value, "_native", value)


