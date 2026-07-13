

from smoke.PLACE_HOLDER_SKIPPED import PLACE_HOLDER_SKIPPED


from _native_base import _NativeBase

import generated


class EnableIfTypesSkipped(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], EnableIfTypesSkipped):
            super().__init__(args[0])
        else:
            super().__init__(generated.EnableIfTypesSkipped(*args))

