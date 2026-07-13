

from smoke.BasicStruct import BasicStruct


from _native_base import _NativeBase

import generated


class PlatformNames(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], PlatformNames):
            super().__init__(args[0])
        else:
            super().__init__(generated.PlatformNames(*args))

