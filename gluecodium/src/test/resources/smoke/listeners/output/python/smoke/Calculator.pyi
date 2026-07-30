

from smoke.CalculatorListener import CalculatorListener
import typing

class Calculator:

    @staticmethod
    def register_listener(listener: CalculatorListener):
        ...

    @staticmethod
    def unregister_listener(listener: CalculatorListener):
        ...

