

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional

from smoke.EnumsExternal_Enum import EnumsExternal_Enum

from _native_base import _NativeBase

import generated


class Enums(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    @staticmethod
    def method_with_external_enum(input: EnumsExternal_Enum):
        """"""
        generated.smoke_Enums.method_with_external_enum(_unwrap(input, EnumsExternal_Enum))

