



from _native_base import _NativeBase

import generated


class NameClashLists(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.NameClashLists):
            super().__init__(args[0])
        else:
            super().__init__(generated.NameClashLists(*[getattr(arg, "_native", arg) for arg in args]))


    @property
    def field_a(self) -> list[Alphabet]:
        """"""
        return self._native.field_a
    @field_a.setter
    def field_a(self, value: list[Alphabet]):
      self._native.field_a = getattr(value, "_native", value)



    @property
    def field_b(self) -> list[Alphabet]:
        """"""
        return self._native.field_b
    @field_b.setter
    def field_b(self, value: list[Alphabet]):
      self._native.field_b = getattr(value, "_native", value)


