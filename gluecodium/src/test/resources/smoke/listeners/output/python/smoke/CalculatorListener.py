

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase, _install_callback_adapters, _unwrap_struct_args, _mark_callback_base, _struct_key
from enum import Enum
from typing import Optional
import generated

from smoke.CalculationResult import CalculationResult

@_mark_callback_base
class CalculatorListener(generated.smoke_CalculatorListener):
    @classmethod
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        _install_callback_adapters(cls, __class__, [
            ("on_calculation_result", "__gluecodium_callback_736d6f6b652e43616c63756c61746f724c697374656e65722e6f6e43616c63756c6174696f6e526573756c74", "method", None,
             lambda: ([float], None)),
            ("on_calculation_result_const", "__gluecodium_callback_736d6f6b652e43616c63756c61746f724c697374656e65722e6f6e43616c63756c6174696f6e526573756c74436f6e7374", "method", None,
             lambda: ([float], None)),
            ("on_calculation_result_struct", "__gluecodium_callback_736d6f6b652e43616c63756c61746f724c697374656e65722e6f6e43616c63756c6174696f6e526573756c74537472756374", "method", None,
             lambda: ([CalculatorListener.ResultStruct], None)),
            ("on_calculation_result_array", "__gluecodium_callback_736d6f6b652e43616c63756c61746f724c697374656e65722e6f6e43616c63756c6174696f6e526573756c744172726179", "method", None,
             lambda: ([list[float]], None)),
            ("on_calculation_result_map", "__gluecodium_callback_736d6f6b652e43616c63756c61746f724c697374656e65722e6f6e43616c63756c6174696f6e526573756c744d6170", "method", None,
             lambda: ([dict[str, float]], None)),
            ("on_calculation_result_instance", "__gluecodium_callback_736d6f6b652e43616c63756c61746f724c697374656e65722e6f6e43616c63756c6174696f6e526573756c74496e7374616e6365", "method", None,
             lambda: ([CalculationResult], None)),
        ])
    def __init__(self, native=None):
        # Subclass the native pybind11 type so that a Python override of an interface
        # method is dispatched through the generated trampoline. When `native` is an
        # existing native instance (returned by a factory), adopt it via the generated
        # adoption constructor and retain the original native object for calls back into
        # C++; otherwise construct a fresh trampoline.
        if native is not None and isinstance(native, generated.smoke_CalculatorListener):
            super().__init__(native)
            self._native = native
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
            if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_CalculatorListener.ResultStruct):
                super().__init__(args[0])
            else:
                super().__init__(generated.smoke_CalculatorListener.ResultStruct(
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
