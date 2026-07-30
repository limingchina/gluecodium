

from smoke.CalculationResult import CalculationResult
from smoke.CalculatorListenerResultStruct import CalculatorListenerResultStruct
import typing

class CalculatorListener:

    def on_calculation_result(self, calculation_result: float):
        ...

    def on_calculation_result_const(self, calculation_result: float):
        ...

    def on_calculation_result_struct(self, calculation_result: CalculatorListenerResultStruct):
        ...

    def on_calculation_result_array(self, calculation_result: list[float]):
        ...

    def on_calculation_result_map(self, calculation_results: dict[str, float]):
        ...

    def on_calculation_result_instance(self, calculation_result: CalculationResult):
        ...

