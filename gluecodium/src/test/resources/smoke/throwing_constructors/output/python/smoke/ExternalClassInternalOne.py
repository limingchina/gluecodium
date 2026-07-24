

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional

from smoke.ExternalClassConstructorExploded import ExternalClassConstructorExploded
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
        native_result = generated.ExternalClassInternalOne.create(*[_unwrap(a) for a in args])
        return ExternalClassInternalOne(native_result)


