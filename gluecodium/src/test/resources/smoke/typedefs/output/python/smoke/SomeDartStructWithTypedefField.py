

from __future__ import annotations

from smoke.list[float] import list[float]


from _native_base import _NativeBase

import generated


class SomeDartStructWithTypedefField(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], SomeDartStructWithTypedefField):
            super().__init__(args[0])
        else:
            super().__init__(generated.SomeDartStructWithTypedefField(*args))


    @property
    def some_field(self) -> list[float]:
        """"""
        return self._native.some_field

    @some_field.setter
    def some_field(self, value: list[float]):
        self._native.some_field = value


