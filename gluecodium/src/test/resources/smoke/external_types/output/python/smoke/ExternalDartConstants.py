

from __future__ import annotations

from smoke.BIG import BIG
from smoke.Rectangle import Rectangle
from smoke.SMALL import SMALL


from _native_base import _NativeBase

import generated


class ExternalDartConstants(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], ExternalDartConstants):
            super().__init__(args[0])
        else:
            super().__init__(generated.ExternalDartConstants(*args))

