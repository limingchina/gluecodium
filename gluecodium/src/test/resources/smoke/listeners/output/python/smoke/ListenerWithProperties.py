

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase
from enum import Enum
from typing import Optional
import generated

from smoke.CalculationResult import CalculationResult

class ListenerWithProperties(generated.smoke_ListenerWithProperties):
    def __init__(self, native=None):
        # Subclass the native pybind11 type so that a Python override of an interface
        # method is dispatched through the generated trampoline. When `native` is an
        # existing native instance (returned by a factory), adopt it via the generated
        # adoption constructor; otherwise construct a fresh trampoline. `self._native`
        # aliases the wrapper itself so the rest of the generated code can reach the
        # native object uniformly (e.g. when passing this interface back into a C++
        # call site).
        if native is not None and isinstance(native, generated.smoke_ListenerWithProperties):
            super().__init__(native)
        else:
            super().__init__()
        self._native = self

    @property
    def message(self) -> str:
        return _wrap(generated.smoke_ListenerWithProperties.message.fget(self), str)

    @message.setter
    def message(self, value: str):
        generated.smoke_ListenerWithProperties.message.fset(self, _unwrap(value, str))

    @property
    def packed_message(self) -> CalculationResult:
        return _wrap(generated.smoke_ListenerWithProperties.packed_message.fget(self), CalculationResult)

    @packed_message.setter
    def packed_message(self, value: CalculationResult):
        generated.smoke_ListenerWithProperties.packed_message.fset(self, _unwrap(value, CalculationResult))

    @property
    def structured_message(self) -> ListenerWithProperties.ResultStruct:
        return _wrap(generated.smoke_ListenerWithProperties.structured_message.fget(self), ListenerWithProperties.ResultStruct)

    @structured_message.setter
    def structured_message(self, value: ListenerWithProperties.ResultStruct):
        generated.smoke_ListenerWithProperties.structured_message.fset(self, _unwrap(value, ListenerWithProperties.ResultStruct))

    @property
    def enumerated_message(self) -> ListenerWithProperties.ResultEnum:
        return _wrap(generated.smoke_ListenerWithProperties.enumerated_message.fget(self), ListenerWithProperties.ResultEnum)

    @enumerated_message.setter
    def enumerated_message(self, value: ListenerWithProperties.ResultEnum):
        generated.smoke_ListenerWithProperties.enumerated_message.fset(self, _unwrap(value, ListenerWithProperties.ResultEnum))

    @property
    def arrayed_message(self) -> list[str]:
        return _wrap(generated.smoke_ListenerWithProperties.arrayed_message.fget(self), list[str])

    @arrayed_message.setter
    def arrayed_message(self, value: list[str]):
        generated.smoke_ListenerWithProperties.arrayed_message.fset(self, _unwrap(value, list[str]))

    @property
    def mapped_message(self) -> dict[str, float]:
        return _wrap(generated.smoke_ListenerWithProperties.mapped_message.fget(self), dict[str, float])

    @mapped_message.setter
    def mapped_message(self, value: dict[str, float]):
        generated.smoke_ListenerWithProperties.mapped_message.fset(self, _unwrap(value, dict[str, float]))

    @property
    def buffered_message(self) -> bytes:
        return _wrap(generated.smoke_ListenerWithProperties.buffered_message.fget(self), bytes)

    @buffered_message.setter
    def buffered_message(self, value: bytes):
        generated.smoke_ListenerWithProperties.buffered_message.fset(self, _unwrap(value, bytes))

    class ResultStruct(_NativeBase):
        def __init__(self, *args, **kwargs):
            if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_ListenerWithPropertiesResultStruct):
                super().__init__(args[0])
            else:
                super().__init__(generated.smoke_ListenerWithPropertiesResultStruct(
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
    
        NONE = generated.smoke_ListenerWithPropertiesResultEnum.NONE
        RESULT = generated.smoke_ListenerWithPropertiesResultEnum.RESULT
    
        @property
        def _native(self):
            return self.value
    
    
    
    StringToDouble = dict[str, float]
    
    

