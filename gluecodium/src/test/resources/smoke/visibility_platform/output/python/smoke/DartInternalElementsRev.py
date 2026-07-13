

from __future__ import annotations



from _native_base import _NativeBase

import generated


class DartInternalElementsRev(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], DartInternalElementsRev):
            super().__init__(args[0])
        else:
            super().__init__(generated.DartInternalElementsRev(*args))


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

