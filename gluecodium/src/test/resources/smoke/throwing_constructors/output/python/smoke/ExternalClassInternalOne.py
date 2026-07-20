

from __future__ import annotations

from smoke.ExternalClassErrorEnum import ExternalClassErrorEnum

from _native_base import _NativeBase

import generated


class ExternalClassInternalOne(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    @staticmethod
    def create(*args, **kwargs) -> ExternalClassInternalOne:
        """"""
        native_result = generated.ExternalClassInternalOne.create(*[getattr(a, "_native", a) for a in args])
        return ExternalClassInternalOne(native_result)


