


from _native_base import _NativeBase


class AsyncWithSkips(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    def make_shared_instance(self, android_context: str):
        """"""
        return self._native.make_shared_instance(android_context)


    def make_shared_instance(self):
        """"""
        return self._native.make_shared_instance()

