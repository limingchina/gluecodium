



from _native_base import _NativeBase

import generated


class NoCacheInterface(_NativeBase):
    """"""

    def __init__(self, native=None):
        if isinstance(native, NoCacheInterface):
            super().__init__(native)
        else:
            super().__init__(generated.NoCacheInterface())


    def foo(self):
        """"""
        return self._native.foo()

