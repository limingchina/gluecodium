

from __future__ import annotations

from smoke.CalculationResult import CalculationResult
from smoke.CalculatorListenerResultStruct import CalculatorListenerResultStruct


import generated


class CalculatorListener(generated.CalculatorListener):
    """"""

    def __init__(self, native=None):
        # Subclass the native pybind11 type so that a Python override of an interface
        # method is dispatched through the generated trampoline. When `native` is an
        # existing native instance (returned by a factory), adopt it via the generated
        # adoption constructor; otherwise construct a fresh trampoline. `self._native`
        # aliases the wrapper itself so the rest of the generated code can reach the
        # native object uniformly (e.g. when passing this interface back into a C++
        # call site).
        if native is not None and isinstance(native, generated.CalculatorListener):
            super().__init__(native)
        else:
            super().__init__()
        self._native = self

    def on_calculation_result(self, calculation_result: float):
        """"""
        return generated.CalculatorListener.on_calculation_result(self, calculation_result)

    def on_calculation_result_const(self, calculation_result: float):
        """"""
        return generated.CalculatorListener.on_calculation_result_const(self, calculation_result)

    def on_calculation_result_struct(self, calculation_result: CalculatorListenerResultStruct):
        """"""
        return generated.CalculatorListener.on_calculation_result_struct(self, calculation_result._native)

    def on_calculation_result_array(self, calculation_result: list[float]):
        """"""
        return generated.CalculatorListener.on_calculation_result_array(self, calculation_result)

    def on_calculation_result_map(self, calculation_results: dict[str, float]):
        """"""
        return generated.CalculatorListener.on_calculation_result_map(self, calculation_results)

    def on_calculation_result_instance(self, calculation_result: CalculationResult):
        """"""
        return generated.CalculatorListener.on_calculation_result_instance(self, calculation_result._native)

