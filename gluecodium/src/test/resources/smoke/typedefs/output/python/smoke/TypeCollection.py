

from __future__ import annotations

from smoke.Point import Point
from smoke.int import int


from _native_base import _NativeBase

import generated


class TypeCollection(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], TypeCollection):
            super().__init__(args[0])
        else:
            super().__init__(generated.TypeCollection(*args))


INVALID_STORAGE_ID = 0

