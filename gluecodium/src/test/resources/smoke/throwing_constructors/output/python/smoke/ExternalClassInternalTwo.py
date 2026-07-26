

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional

from smoke.ExternalClassConstructorExploded import ExternalClassConstructorExploded
from smoke.ExternalClassErrorEnum import ExternalClassErrorEnum

from _native_base import _NativeBase

import generated


class ExternalClassInternalTwo(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    @staticmethod
    def create() -> ExternalClassInternalTwo:
        """"""
        native_result = generated.smoke_ExternalClassInternalTwo.create()
        return ExternalClassInternalTwo(native_result)

