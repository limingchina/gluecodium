

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
        generated.Calculator.register_listener(listener._native)

    @staticmethod
    def unregister_listener(listener: CalculatorListener):
        """"""
        generated.Calculator.unregister_listener(listener._native)

