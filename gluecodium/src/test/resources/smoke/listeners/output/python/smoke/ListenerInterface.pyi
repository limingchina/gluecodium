



from _native_base import _NativeBase

import generated


class ListenerInterface(_NativeBase):
    """"""

    def __init__(self, native=None):
        if isinstance(native, ListenerInterface):
            super().__init__(native)
        else:
            super().__init__(generated.ListenerInterface())


    def notify(self):
        """"""
        return self._native.notify()

