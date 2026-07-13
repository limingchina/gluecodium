

from __future__ import annotations



from _native_base import _NativeBase

import generated


class ExcludedCommentsInterface(_NativeBase):
    """This is some very useful interface."""

    def __init__(self, native=None):
        if isinstance(native, ExcludedCommentsInterface):
            super().__init__(native)
        else:
            super().__init__(generated.ExcludedCommentsInterface())

