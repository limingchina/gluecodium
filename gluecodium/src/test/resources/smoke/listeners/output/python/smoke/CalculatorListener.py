

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase
from enum import Enum
from typing import Optional
import generated

from smoke.CalculationResult import CalculationResult

class CalculatorListener(generated.smoke_CalculatorListener):
    def __init__(self, native=None):
        # Subclass the native pybind11 type so that a Python override of an interface
        # method is dispatched through the generated trampoline. When `native` is an
        # existing native instance (returned by a factory), adopt it via the generated
        # adoption constructor; otherwise construct a fresh trampoline. `self._native`
        # aliases the wrapper itself so the rest of the generated code can reach the
        # native object uniformly (e.g. when passing this interface back into a C++
        # call site).
        if native is not None and isinstance(native, generated.smoke_CalculatorListener):
            super().__init__(native)
        else:
            super().__init__()
        self._native = self

    def on_calculation_result(self, calculation_result: float):
        return _wrap(generated.smoke_CalculatorListener.on_calculation_result(self, _unwrap(calculation_result, float)), None)

    def on_calculation_result_const(self, calculation_result: float):
        return _wrap(generated.smoke_CalculatorListener.on_calculation_result_const(self, _unwrap(calculation_result, float)), None)

    def on_calculation_result_struct(self, calculation_result: CalculatorListener.ResultStruct):
        return _wrap(generated.smoke_CalculatorListener.on_calculation_result_struct(self, _unwrap(calculation_result, CalculatorListener.ResultStruct)), None)

    def on_calculation_result_array(self, calculation_result: list[float]):
        return _wrap(generated.smoke_CalculatorListener.on_calculation_result_array(self, _unwrap(calculation_result, list[float])), None)

    def on_calculation_result_map(self, calculation_results: dict[str, float]):
        return _wrap(generated.smoke_CalculatorListener.on_calculation_result_map(self, _unwrap(calculation_results, dict[str, float])), None)

    def on_calculation_result_instance(self, calculation_result: CalculationResult):
        return _wrap(generated.smoke_CalculatorListener.on_calculation_result_instance(self, _unwrap(calculation_result, CalculationResult)), None)

    class ResultStruct(_NativeBase):
        def __init__(self, *args, **kwargs):
            if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_CalculatorListenerResultStruct):
                super().__init__(args[0])
            else:
                super().__init__(generated.smoke_CalculatorListenerResultStruct(
                    *[_unwrap(arg) for arg in args],
                    **{k: _unwrap(v) for k, v in kwargs.items()}
                ))
    
        @property
        def result(self) -> float:
            return _wrap(self._native.result, float)
        @result.setter
        def result(self, value: float):
          self._native.result = _unwrap(value, float)
    
    
    
    
    NamedCalculationResults = dict[str, float]
    
    

