

from smoke.CalculatorListener import CalculatorListener

from _native_base import _NativeBase


class Calculator(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    def register_listener(self, listener: CalculatorListener):
        """"""
        return self._native.register_listener(listener)


    def unregister_listener(self, listener: CalculatorListener):
        """"""
        return self._native.unregister_listener(listener)

