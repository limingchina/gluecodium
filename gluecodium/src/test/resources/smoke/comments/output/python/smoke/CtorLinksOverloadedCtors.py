

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper
from typing import Optional


from _native_base import _NativeBase

import generated


class CtorLinksOverloadedCtors(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    @staticmethod
    def create(*args, **kwargs) -> CtorLinksOverloadedCtors:
        """"""
        native_result = generated.smoke_CtorLinksOverloadedCtors.create(*[_unwrap(a) for a in args])
        return _get_or_create_wrapper(native_result, CtorLinksOverloadedCtors)


