


from _native_base import _NativeBase


class ParentClass(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    def parent_fun(self):
        """"""
        return self._native.parent_fun()


    @property
    def parent_property(self) -> str:
        """"""
        return self._native.parent_property


