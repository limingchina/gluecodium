

from __future__ import annotations

from smoke.ConstructorExplodedError import ConstructorExplodedError
from smoke.ErrorEnum import ErrorEnum
from smoke.InternalOne import InternalOne
from smoke.InternalTwo import InternalTwo


from _native_base import _NativeBase

import generated


class ExternalClass(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    @staticmethod
    def create() -> ExternalClass:
        """"""
        native_result = generated.ExternalClass.create()
        return ExternalClass(native_result)

