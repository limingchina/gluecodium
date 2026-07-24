

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional



from _native_base import _NativeBase

import generated


class CrossFileConstants(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.CrossFileConstants):
            super().__init__(args[0])
        else:
            super().__init__(generated.CrossFileConstants(*[_unwrap(arg) for arg in args]))


    FOO_BAR = StateEnum.ON

