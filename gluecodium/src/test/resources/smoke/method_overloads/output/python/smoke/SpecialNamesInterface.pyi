

from smoke.Callback import Callback

from _native_base import _NativeBase


class SpecialNamesInterface(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    def dispatch(self, callback: Callback):
        """"""
        return self._native.dispatch(callback)

