

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase
from enum import Enum
from typing import Optional
import generated

from smoke.CalculationResult import CalculationResult

class ListenersWithReturnValues(generated.smoke_ListenersWithReturnValues):
    def __init__(self, native=None):
        # Subclass the native pybind11 type so that a Python override of an interface
        # method is dispatched through the generated trampoline. When `native` is an
        # existing native instance (returned by a factory), adopt it via the generated
        # adoption constructor and retain the original native object for calls back into
        # C++; otherwise construct a fresh trampoline.
        if native is not None and isinstance(native, generated.smoke_ListenersWithReturnValues):
            super().__init__(native)
            self._native = native
        else:
            super().__init__()
            self._native = self

    def fetch_data_double(self) -> float:
        return _wrap(generated.smoke_ListenersWithReturnValues.fetch_data_double(self), float)

    def fetch_data_string(self) -> str:
        return _wrap(generated.smoke_ListenersWithReturnValues.fetch_data_string(self), str)

    def fetch_data_struct(self) -> ListenersWithReturnValues.ResultStruct:
        return _wrap(generated.smoke_ListenersWithReturnValues.fetch_data_struct(self), ListenersWithReturnValues.ResultStruct)

    def fetch_data_enum(self) -> ListenersWithReturnValues.ResultEnum:
        return _wrap(generated.smoke_ListenersWithReturnValues.fetch_data_enum(self), ListenersWithReturnValues.ResultEnum)

    def fetch_data_array(self) -> list[float]:
        return _wrap(generated.smoke_ListenersWithReturnValues.fetch_data_array(self), list[float])

    def fetch_data_map(self) -> dict[str, float]:
        return _wrap(generated.smoke_ListenersWithReturnValues.fetch_data_map(self), dict[str, float])

    def fetch_data_instance(self) -> CalculationResult:
        return _wrap(generated.smoke_ListenersWithReturnValues.fetch_data_instance(self), CalculationResult)

    class ResultStruct(_NativeBase):
        def __init__(self, *args, **kwargs):
            if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_ListenersWithReturnValues.ResultStruct):
                super().__init__(args[0])
            else:
                super().__init__(generated.smoke_ListenersWithReturnValues.ResultStruct(
                    *[_unwrap(arg) for arg in args],
                    **{k: _unwrap(v) for k, v in kwargs.items()}
                ))
    
        @property
        def result(self) -> float:
            return _wrap(self._native.result, float)
        @result.setter
        def result(self, value: float):
          self._native.result = _unwrap(value, float)
    
    
    
    
    class ResultEnum(Enum):
    
        NONE = generated.smoke_ListenersWithReturnValues.ResultEnum.NONE
        RESULT = generated.smoke_ListenersWithReturnValues.ResultEnum.RESULT
    
        @property
        def _native(self):
            return self.value
    
    
    
    StringToDouble = dict[str, float]
    
    

