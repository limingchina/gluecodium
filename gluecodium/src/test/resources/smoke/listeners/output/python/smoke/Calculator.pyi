

from smoke.CalculatorListener import CalculatorListener
import typing

from _native_base import _NativeBase

import generated


class Calculator(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    @staticmethod
    def register_listener(listener: CalculatorListener): ...

    @staticmethod
    def unregister_listener(listener: CalculatorListener): ...

