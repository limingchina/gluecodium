

from __future__ import annotations

from smoke.InterfaceWithLambda import InterfaceWithLambda


from _native_base import _NativeBase

import generated


class ChildClassWithLambda(
    InterfaceWithLambda)(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

