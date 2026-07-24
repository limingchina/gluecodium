

import typing


from _native_base import _NativeBase

import generated


class SkipTypesTags(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.SkipTypesTags):
            super().__init__(args[0])
        else:
            super().__init__(generated.SkipTypesTags(*[_unwrap(arg) for arg in args]))


    PLACE_HOLDER = True

