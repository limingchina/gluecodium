


from _native_base import _NativeBase


class InterfaceWithStatic(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    def regular_function(self) -> str:
        """"""
        return self._native.regular_function()


    def static_function(self) -> str:
        """"""
        return self._native.static_function()


    @property
    def regular_property(self) -> str:
        """"""
        return self._native.regular_property



    @property
    def static_property(self) -> str:
        """"""
        return self._native.static_property


