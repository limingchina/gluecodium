

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional

from package.typesenum import typesenum
from package.typesstruct import typesstruct


from _native_base import _NativeBase

import generated


class Types(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.package_Types):
            super().__init__(args[0])
        else:
            super().__init__(generated.package_Types(*[_unwrap(arg) for arg in args]))


    CONST = typesenum.NA_N

