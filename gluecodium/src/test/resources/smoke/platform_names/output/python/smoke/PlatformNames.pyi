

from smoke.PlatformNamesBasicStruct import PlatformNamesBasicStruct
import typing


from _native_base import _NativeBase

import generated


class PlatformNames(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.PlatformNames):
            super().__init__(args[0])
        else:
            super().__init__(generated.PlatformNames(*[_unwrap(arg) for arg in args]))

