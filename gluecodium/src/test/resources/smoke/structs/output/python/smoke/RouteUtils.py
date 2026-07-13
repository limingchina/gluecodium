

from __future__ import annotations



from _native_base import _NativeBase

import generated


class RouteUtils(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], RouteUtils):
            super().__init__(args[0])
        else:
            super().__init__(generated.RouteUtils(*args))

