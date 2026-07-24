

from smoke.ExternalClassConstructorExploded import ExternalClassConstructorExploded
from smoke.ExternalClassErrorEnum import ExternalClassErrorEnum
import typing

from _native_base import _NativeBase

import generated


class ExternalClassInternalTwo(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    @staticmethod
    def create() -> ExternalClassInternalTwo: ...

