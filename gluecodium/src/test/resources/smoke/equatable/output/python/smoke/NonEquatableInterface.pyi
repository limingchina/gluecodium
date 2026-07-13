



from _native_base import _NativeBase

import generated


class NonEquatableInterface(_NativeBase):
    """"""

    def __init__(self, native=None):
        if isinstance(native, NonEquatableInterface):
            super().__init__(native)
        else:
            super().__init__(generated.NonEquatableInterface())

