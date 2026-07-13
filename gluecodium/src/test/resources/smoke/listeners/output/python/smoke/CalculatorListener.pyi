

from smoke.CalculationResult import CalculationResult
from smoke.ResultStruct import ResultStruct
from smoke.dict[str, float] import dict[str, float]


from _native_base import _NativeBase

import generated


class CalculatorListener(_NativeBase):
    """"""

    def __init__(self, native=None):
        if isinstance(native, CalculatorListener):
            super().__init__(native)
        else:
            super().__init__(generated.CalculatorListener())


    def on_calculation_result(self, calculation_result: float):
        """"""
        return self._native.on_calculation_result(calculation_result)


    def on_calculation_result_const(self, calculation_result: float):
        """"""
        return self._native.on_calculation_result_const(calculation_result)


    def on_calculation_result_struct(self, calculation_result: ResultStruct):
        """"""
        return self._native.on_calculation_result_struct(calculation_result._native)


    def on_calculation_result_array(self, calculation_result: list[float]):
        """"""
        return self._native.on_calculation_result_array(calculation_result)


    def on_calculation_result_map(self, calculation_results: dict[str, float]):
        """"""
        return self._native.on_calculation_result_map(calculation_results._native)


    def on_calculation_result_instance(self, calculation_result: CalculationResult):
        """"""
        return self._native.on_calculation_result_instance(calculation_result._native)

