

from __future__ import annotations



from _native_base import _NativeBase

import generated


class NameClashLists(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], NameClashLists):
            super().__init__(args[0])
        else:
            super().__init__(generated.NameClashLists(*args))


    @property
    def field_a(self) -> list[Alphabet]:
        """"""
        return self._native.field_a

    @field_a.setter
    def field_a(self, value: list[Alphabet]):
        self._native.field_a = value



    @property
    def field_b(self) -> list[Alphabet]:
        """"""
        return self._native.field_b

    @field_b.setter
    def field_b(self, value: list[Alphabet]):
        self._native.field_b = value


