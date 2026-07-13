

from __future__ import annotations



from _native_base import _NativeBase

import generated


class DartInternalElementsEnabled(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], DartInternalElementsEnabled):
            super().__init__(args[0])
        else:
            super().__init__(generated.DartInternalElementsEnabled(*args))


    @property
    def bool_field(self) -> bool:
        """"""
        return self._native.bool_field

    @bool_field.setter
    def bool_field(self, value: bool):
        self._native.bool_field = value



    @property
    def string_field(self) -> str:
        """"""
        return self._native.string_field

    @string_field.setter
    def string_field(self, value: str):
        self._native.string_field = value



    def foo(self):
        """"""
        return self._native.foo()

