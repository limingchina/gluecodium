

from smoke.ParentInterface import ParentInterface


from _native_base import _NativeBase

import generated


class ChildInterface(_NativeBase):
    """"""

    def __init__(self, native=None):
        if isinstance(native, ChildInterface):
            super().__init__(native)
        else:
            super().__init__(generated.ChildInterface())


    def child_method(self):
        """"""
        return self._native.child_method()

