

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional


from _native_base import _NativeBase

import generated


class CtorLinksSingleCtor(_NativeBase):
    """This class has just one constructor [create]."""

    def __init__(self, native):
        super().__init__(native)

    @staticmethod
    def create() -> CtorLinksSingleCtor:
        """"""
        native_result = generated.CtorLinksSingleCtor.create()
        return CtorLinksSingleCtor(native_result)

