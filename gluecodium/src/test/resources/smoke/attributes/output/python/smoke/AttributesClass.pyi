

from smoke.PI import PI

from _native_base import _NativeBase


class AttributesClass(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    def very_fun(self, param: str):
        """"""
        return self._native.very_fun(param)


    @property
    def prop(self) -> str:
        """"""
        return self._native.prop


