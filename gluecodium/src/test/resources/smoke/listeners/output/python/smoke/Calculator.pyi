

from smoke.CalculatorListener import CalculatorListener
from enum import Enum
import typing
from typing import Optional

class Calculator:

    @staticmethod
    def register_listener(listener: CalculatorListener):
        ...

    @staticmethod
    def unregister_listener(listener: CalculatorListener):
        ...
