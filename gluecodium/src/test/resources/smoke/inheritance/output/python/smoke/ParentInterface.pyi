


from _native_base import _NativeBase


class ParentInterface(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    def root_method(self):
        """"""
        return self._native.root_method()


    @property
    def root_property(self) -> str:
        """"""
        return self._native.root_property


