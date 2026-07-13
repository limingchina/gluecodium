


from _native_base import _NativeBase


class ParentClass(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    def parent_function(self):
        """"""
        return self._native.parent_function()


    @property
    def parent_property(self) -> str:
        """"""
        return self._native.parent_property


