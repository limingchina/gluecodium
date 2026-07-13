

from smoke.CalculationResult import CalculationResult
from smoke.ResultStruct import ResultStruct
from smoke.dict[str, float] import dict[str, float]

class CalculatorListener:
    """"""

    def __init__(self, native):
        self._native = native


    def on_calculation_result(self, calculation_result: float):
        """"""
        return self._native.on_calculation_result(calculation_result)


    def on_calculation_result_const(self, calculation_result: float):
        """"""
        return self._native.on_calculation_result_const(calculation_result)


    def on_calculation_result_struct(self, calculation_result: ResultStruct):
        """"""
        return self._native.on_calculation_result_struct(calculation_result)


    def on_calculation_result_array(self, calculation_result: list[float]):
        """"""
        return self._native.on_calculation_result_array(calculation_result)


    def on_calculation_result_map(self, calculation_results: dict[str, float]):
        """"""
        return self._native.on_calculation_result_map(calculation_results)


    def on_calculation_result_instance(self, calculation_result: CalculationResult):
        """"""
        return self._native.on_calculation_result_instance(calculation_result)

