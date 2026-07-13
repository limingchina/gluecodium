

from smoke.PI import PI

from _native_base import _NativeBase


class AttributesWithDeprecated(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    def very_fun(self):
        """"""
        return self._native.very_fun()


    @property
    def prop(self) -> str:
        """"""
        return self._native.prop


