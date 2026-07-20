

from __future__ import annotations


from _native_base import _NativeBase

import generated


class CtorLinksOverloadedCtors(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    @staticmethod
    def create(*args, **kwargs) -> CtorLinksOverloadedCtors:
        """"""
        native_result = generated.CtorLinksOverloadedCtors.create(*[getattr(a, "_native", a) for a in args])
        return CtorLinksOverloadedCtors(native_result)


