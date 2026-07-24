

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional

from smoke.EnableIfTypesEnabledEnableMe import EnableIfTypesEnabledEnableMe


from _native_base import _NativeBase

import generated


class EnableIfTypesEnabled(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.EnableIfTypesEnabled):
            super().__init__(args[0])
        else:
            super().__init__(generated.EnableIfTypesEnabled(*[_unwrap(arg) for arg in args]))


    PLACE_HOLDER_ENABLED = True

