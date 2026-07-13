


from _native_base import _NativeBase


class JavaInternalPropertyRev(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    @property
    def app_context(self):
        """"""
        return self._native.app_context


