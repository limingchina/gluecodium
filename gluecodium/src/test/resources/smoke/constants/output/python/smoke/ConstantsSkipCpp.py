

from __future__ import annotations



from _native_base import _NativeBase

import generated


class ConstantsSkipCpp(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.ConstantsSkipCpp):
            super().__init__(args[0])
        else:
            super().__init__(generated.ConstantsSkipCpp(*[getattr(arg, "_native", arg) for arg in args]))


    BOOL_CONSTANT = True


    INT_CONSTANT = -11

