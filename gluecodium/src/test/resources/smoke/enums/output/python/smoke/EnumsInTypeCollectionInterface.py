

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional

from smoke.EnumsInTypeCollectionTCEnum import EnumsInTypeCollectionTCEnum

from _native_base import _NativeBase

import generated


class EnumsInTypeCollectionInterface(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    @staticmethod
    def flip_enum_value(input: EnumsInTypeCollectionTCEnum) -> EnumsInTypeCollectionTCEnum:
        """"""
        native_result = generated.smoke_EnumsInTypeCollectionInterface.flip_enum_value(_unwrap(input, EnumsInTypeCollectionTCEnum))
        return EnumsInTypeCollectionTCEnum(native_result)

