

from __future__ import annotations

from smoke.BOOL_CONSTANT import BOOL_CONSTANT
from smoke.INT_CONSTANT import INT_CONSTANT


from _native_base import _NativeBase

import generated


class ConstantsSkipCpp(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], ConstantsSkipCpp):
            super().__init__(args[0])
        else:
            super().__init__(generated.ConstantsSkipCpp(*args))

