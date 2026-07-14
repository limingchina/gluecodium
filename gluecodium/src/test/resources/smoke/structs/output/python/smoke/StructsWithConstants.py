

from __future__ import annotations

from smoke.RouteType import RouteType


from _native_base import _NativeBase

import generated


class StructsWithConstants(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], StructsWithConstants):
            super().__init__(args[0])
        else:
            super().__init__(generated.StructsWithConstants(*[getattr(arg, "_native", arg) for arg in args]))

