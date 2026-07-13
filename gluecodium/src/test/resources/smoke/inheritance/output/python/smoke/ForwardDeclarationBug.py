

from __future__ import annotations

from smoke.ParentClass import ParentClass


from _native_base import _NativeBase

import generated


class ForwardDeclarationBug(
    ParentClass)(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    def foo(self, bar: ParentClass):
        """"""
        return self._native.foo(bar._native)

