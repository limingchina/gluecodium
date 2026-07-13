

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

from enum import Enum


class ExternalEnum(Enum):
    """"""

    FOO_VALUE = 0
    BAR_VALUE = 1

from enum import Enum


class VeryExternalEnum(Enum):
    """"""

    FOO = 0
    BAR = 1

