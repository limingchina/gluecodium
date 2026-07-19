



from _native_base import _NativeBase

import generated


class FieldConstructorsSkipTag(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.FieldConstructorsSkipTag):
            super().__init__(args[0])
        else:
            super().__init__(generated.FieldConstructorsSkipTag(*[getattr(arg, "_native", arg) for arg in args]))


    @property
    def field1(self) -> str:
        """"""
        return self._native.field1
    @field1.setter
    def field1(self, value: str):
      self._native.field1 = getattr(value, "_native", value)


