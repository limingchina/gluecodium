



from _native_base import _NativeBase

import generated


class OuterInternalInterface(_NativeBase):
    """"""

    def __init__(self, native=None):
        if isinstance(native, OuterInternalInterface):
            super().__init__(native)
        else:
            super().__init__(generated.OuterInternalInterface())


    def some_function(self) -> int:
        """"""
        return self._native.some_function()

