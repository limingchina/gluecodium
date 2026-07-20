

from smoke.TypeCollectionPoint import TypeCollectionPoint
import typing


from _native_base import _NativeBase

import generated


class TypeCollection(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.TypeCollection):
            super().__init__(args[0])
        else:
            super().__init__(generated.TypeCollection(*[getattr(arg, "_native", arg) for arg in args]))

