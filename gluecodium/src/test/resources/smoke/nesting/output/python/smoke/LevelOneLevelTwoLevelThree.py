

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper
from typing import Optional

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
        return _wrap(self._native.foo(_unwrap(input, OuterClassInnerInterface)), OuterInterfaceInnerClass)

