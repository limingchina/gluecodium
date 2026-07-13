


from _native_base import _NativeBase


class AsyncRenamed(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    def dispose(self):
        """"""
        return self._native.dispose()

