

from __future__ import annotations

from smoke.CalculatorListener import CalculatorListener


from _native_base import _NativeBase

import generated


class Calculator(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    @staticmethod

    def register_listener(listener: CalculatorListener):
        """"""
        native_result = generated.Calculator.register_listener(listener)
        return None(native_result)

    @staticmethod

    def unregister_listener(listener: CalculatorListener):
        """"""
        native_result = generated.Calculator.unregister_listener(listener)
        return None(native_result)

