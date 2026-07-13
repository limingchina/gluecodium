

from __future__ import annotations



from _native_base import _NativeBase

import generated


class JavaExternalCtor(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], JavaExternalCtor):
            super().__init__(args[0])
        else:
            super().__init__(generated.JavaExternalCtor(*args))


    @property
    def field(self) -> str:
        """"""
        return self._native.field

    @field.setter
    def field(self, value: str):
        self._native.field = value


    @staticmethod

    def make(field: str) -> JavaExternalCtor:
        """"""
        native_result = generated.JavaExternalCtor.make(field)
        return JavaExternalCtor(native_result)

