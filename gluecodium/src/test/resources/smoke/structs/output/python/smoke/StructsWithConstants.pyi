

from smoke.RouteUtilsRouteType import RouteUtilsRouteType
import typing


from _native_base import _NativeBase

import generated


class StructsWithConstants(_NativeBase):
    """"""

    def __init__(self, *args, **kwargs):
        if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_StructsWithConstants):
            super().__init__(args[0])
        else:
            super().__init__(generated.smoke_StructsWithConstants(
                *[_unwrap(arg) for arg in args],
                **{k: _unwrap(v) for k, v in kwargs.items()}
            ))

