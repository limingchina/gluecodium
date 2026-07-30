

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper
from typing import Optional


from _native_base import _NativeBase

import generated


class CtorLinksSingleCtorWithOneArgument(_NativeBase):
    """This class has just one constructor with one argument [create(Int)]."""
    def __init__(self, native):
        super().__init__(native)

    @staticmethod
    def create(arg: int) -> CtorLinksSingleCtorWithOneArgument:
        native_result = generated.smoke_CtorLinksSingleCtorWithOneArgument.create(_unwrap(arg, int))
        return _get_or_create_wrapper(native_result, CtorLinksSingleCtorWithOneArgument)

