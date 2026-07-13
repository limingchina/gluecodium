

from smoke.CalculatorListener import CalculatorListener

class Calculator:
    """"""

    def __init__(self, native):
        self._native = native


    def register_listener(self, listener: CalculatorListener):
        """"""
        return self._native.register_listener(listener)


    def unregister_listener(self, listener: CalculatorListener):
        """"""
        return self._native.unregister_listener(listener)

