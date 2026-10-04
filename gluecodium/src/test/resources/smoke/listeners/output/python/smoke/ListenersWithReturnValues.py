

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase, _install_callback_adapters, _unwrap_struct_args, _mark_callback_base
from enum import Enum
from typing import Optional
import generated

from smoke.CalculationResult import CalculationResult

@_mark_callback_base
class ListenersWithReturnValues(generated.smoke_ListenersWithReturnValues):
    @classmethod
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        _install_callback_adapters(cls, __class__, [
            ("fetch_data_double", "__gluecodium_callback_736d6f6b652e4c697374656e6572735769746852657475726e56616c7565732e666574636844617461446f75626c65", "method", None,
             lambda: ([], float)),
            ("fetch_data_string", "__gluecodium_callback_736d6f6b652e4c697374656e6572735769746852657475726e56616c7565732e666574636844617461537472696e67", "method", None,
             lambda: ([], str)),
            ("fetch_data_struct", "__gluecodium_callback_736d6f6b652e4c697374656e6572735769746852657475726e56616c7565732e666574636844617461537472756374", "method", None,
             lambda: ([], ListenersWithReturnValues.ResultStruct)),
            ("fetch_data_enum", "__gluecodium_callback_736d6f6b652e4c697374656e6572735769746852657475726e56616c7565732e666574636844617461456e756d", "method", None,
             lambda: ([], ListenersWithReturnValues.ResultEnum)),
            ("fetch_data_array", "__gluecodium_callback_736d6f6b652e4c697374656e6572735769746852657475726e56616c7565732e6665746368446174614172726179", "method", None,
             lambda: ([], list[float])),
            ("fetch_data_map", "__gluecodium_callback_736d6f6b652e4c697374656e6572735769746852657475726e56616c7565732e6665746368446174614d6170", "method", None,
             lambda: ([], dict[str, float])),
            ("fetch_data_instance", "__gluecodium_callback_736d6f6b652e4c697374656e6572735769746852657475726e56616c7565732e666574636844617461496e7374616e6365", "method", None,
             lambda: ([], CalculationResult)),
        ])
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
    
    

