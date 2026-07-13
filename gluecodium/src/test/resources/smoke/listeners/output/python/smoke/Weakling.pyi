

from smoke.ListenerInterface import ListenerInterface

from _native_base import _NativeBase


class Weakling(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    @property
    def listener(self):
        """"""
        return self._native.listener


