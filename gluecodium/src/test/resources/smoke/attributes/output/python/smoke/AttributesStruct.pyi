

from smoke.PI import PI

from _native_base import _NativeBase


class AttributesStruct(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    field: str


    def very_fun(self, param: str):
        """"""
        return self._native.very_fun(param)

