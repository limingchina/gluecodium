

import typing


from _native_base import _NativeBase

import generated


class ExternalEquatable(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.smoke_ExternalEquatable):
            super().__init__(args[0])
        else:
            super().__init__(generated.smoke_ExternalEquatable(*[_unwrap(arg) for arg in args]))

