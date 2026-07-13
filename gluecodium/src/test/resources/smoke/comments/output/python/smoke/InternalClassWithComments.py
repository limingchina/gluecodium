

from __future__ import annotations



from _native_base import _NativeBase

import generated


class InternalClassWithComments(_NativeBase):
    """This looks internal"""

    def __init__(self, native):
        super().__init__(native)

    This is definitely internal
    def do_nothing(self):
        """This is definitely internal"""
        return self._native.do_nothing()

