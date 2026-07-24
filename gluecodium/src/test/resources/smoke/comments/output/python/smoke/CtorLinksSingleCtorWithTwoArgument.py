

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional


from _native_base import _NativeBase

import generated


class CtorLinksSingleCtorWithTwoArgument(_NativeBase):
    """This class has just one constructor with two argument [create(Int, String)]."""

    def __init__(self, native):
        super().__init__(native)

    @staticmethod
    def create(arg: int, arg2: str) -> CtorLinksSingleCtorWithTwoArgument:
        """"""
        native_result = generated.CtorLinksSingleCtorWithTwoArgument.create(_unwrap(arg, int), _unwrap(arg2, str))
        return CtorLinksSingleCtorWithTwoArgument(native_result)

