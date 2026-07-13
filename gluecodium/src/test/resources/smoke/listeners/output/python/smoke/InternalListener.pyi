


from _native_base import _NativeBase


class InternalListener(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    def on_event(self):
        """"""
        return self._native.on_event()

