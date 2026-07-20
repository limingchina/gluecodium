

import typing


from _native_base import _NativeBase

import generated


class BasicTypes(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.BasicTypes):
            super().__init__(args[0])
        else:
            super().__init__(generated.BasicTypes(*[getattr(arg, "_native", arg) for arg in args]))

