


from _native_base import _NativeBase


class ListenerInterface(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    def notify(self):
        """"""
        return self._native.notify()

