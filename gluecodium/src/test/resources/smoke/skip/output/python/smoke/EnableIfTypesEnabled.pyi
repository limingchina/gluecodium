

from smoke.EnableMe import EnableMe
from smoke.PLACE_HOLDER_ENABLED import PLACE_HOLDER_ENABLED


from _native_base import _NativeBase

import generated


class EnableIfTypesEnabled(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], EnableIfTypesEnabled):
            super().__init__(args[0])
        else:
            super().__init__(generated.EnableIfTypesEnabled(*args))

