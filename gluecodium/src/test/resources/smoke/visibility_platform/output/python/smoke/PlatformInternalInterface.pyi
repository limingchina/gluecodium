



from _native_base import _NativeBase

import generated


class PlatformInternalInterface(_NativeBase):
    """"""

    def __init__(self, native=None):
        if isinstance(native, PlatformInternalInterface):
            super().__init__(native)
        else:
            super().__init__(generated.PlatformInternalInterface())

