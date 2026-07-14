

from __future__ import annotations

from smoke.PublicClassInternalStruct import PublicClassInternalStruct


from _native_base import _NativeBase

import generated


class PublicInterface(_NativeBase):
    """"""

    def __init__(self, native=None):
        if isinstance(native, PublicInterface):
            super().__init__(native)
        else:
            super().__init__(generated.PublicInterface())

