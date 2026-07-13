



from _native_base import _NativeBase

import generated


class InternalClass(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    def foo_bar(self):
        """"""
        return self._native.foo_bar()

