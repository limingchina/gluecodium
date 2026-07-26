

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional

from smoke.PlatformNamesBasicStruct import PlatformNamesBasicStruct


from _native_base import _NativeBase

import generated


class PlatformNames(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.smoke_PlatformNames):
            super().__init__(args[0])
        else:
            super().__init__(generated.smoke_PlatformNames(*[_unwrap(arg) for arg in args]))

