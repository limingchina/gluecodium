

from __future__ import annotations

from smoke.LevelOneLevelTwoLevelThreeLevelFour import LevelOneLevelTwoLevelThreeLevelFour
from smoke.OuterClassInnerInterface import OuterClassInnerInterface
from smoke.OuterInterfaceInnerClass import OuterInterfaceInnerClass

from _native_base import _NativeBase

import generated


class LevelOneLevelTwoLevelThree(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    def foo(self, input: OuterClassInnerInterface) -> OuterInterfaceInnerClass:
        """"""
        return self._native.foo(input._native)

