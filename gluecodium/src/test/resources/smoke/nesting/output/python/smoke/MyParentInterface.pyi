



from _native_base import _NativeBase

import generated


class MyParentInterface(_NativeBase):
    """"""

    def __init__(self, native=None):
        if isinstance(native, MyParentInterface):
            super().__init__(native)
        else:
            super().__init__(generated.MyParentInterface())

