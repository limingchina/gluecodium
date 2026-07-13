

from __future__ import annotations



from _native_base import _NativeBase

import generated


class PlatformNamesListener(_NativeBase):
    """"""

    def __init__(self, native=None):
        if isinstance(native, PlatformNamesListener):
            super().__init__(native)
        else:
            super().__init__(generated.PlatformNamesListener())


    def basic_method(self, basic_parameter: str):
        """"""
        return self._native.basic_method(basic_parameter)

