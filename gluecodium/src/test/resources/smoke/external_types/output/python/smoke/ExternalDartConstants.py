

from __future__ import annotations

from smoke.Rectangle import Rectangle


from _native_base import _NativeBase

import generated


class ExternalDartConstants(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.ExternalDartConstants):
            super().__init__(args[0])
        else:
            super().__init__(generated.ExternalDartConstants(*[getattr(arg, "_native", arg) for arg in args]))


    SMALL = {0, 0, 1, 1}


    BIG = {0, 0, 10, 10}

