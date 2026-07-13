

from __future__ import annotations

from smoke.ListenerInterface import ListenerInterface


from _native_base import _NativeBase

import generated


class Weakling(_NativeBase):
    """"""

    def __init__(self, native=None):
        if isinstance(native, Weakling):
            super().__init__(native)
        else:
            super().__init__(generated.Weakling())


    @property
    def listener(self):
        """"""
        return self._native.listener

    @listener.setter
    def listener(self, value):
        self._native.listener = value

