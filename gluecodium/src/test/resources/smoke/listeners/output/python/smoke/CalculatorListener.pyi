

from smoke.CalculationResult import CalculationResult
from enum import Enum
import typing
from typing import Optional

class CalculatorListener:

    def on_calculation_result(self, calculation_result: float):
        ...

    def on_calculation_result_const(self, calculation_result: float):
        ...

    def on_calculation_result_struct(self, calculation_result: CalculatorListener.ResultStruct):
        ...

    def on_calculation_result_array(self, calculation_result: list[float]):
        ...

    def on_calculation_result_map(self, calculation_results: dict[str, float]):
        ...

    def on_calculation_result_instance(self, calculation_result: CalculationResult):
        ...

    class ResultStruct:
        @typing.overload
        def __init__(self) -> None: ...
        @typing.overload
        def __init__(self, result: float) -> None: ...

        result: float



    NamedCalculationResults = dict[str, float]
