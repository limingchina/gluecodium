

from __future__ import annotations

from smoke.StructConstantsNestingStruct import StructConstantsNestingStruct
from smoke.StructConstantsSomeStruct import StructConstantsSomeStruct

from _native_base import _NativeBase

import generated


class StructConstants(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    STRUCT_CONSTANT = {"bar Buzz", 1.41}


    NESTING_STRUCT_CONSTANT = {{"nonsense", -2.82}}

