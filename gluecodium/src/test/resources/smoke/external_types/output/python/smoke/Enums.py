

from __future__ import annotations

from smoke.ExternalEnum import ExternalEnum


from _native_base import _NativeBase

import generated


class Enums(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    @staticmethod

    def method_with_external_enum(input: ExternalEnum):
        """"""
        native_result = generated.Enums.method_with_external_enum(input)
        return None(native_result)

