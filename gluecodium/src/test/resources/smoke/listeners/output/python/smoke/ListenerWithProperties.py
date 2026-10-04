

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase, _install_callback_adapters, _unwrap_struct_args, _mark_callback_base
from enum import Enum
from typing import Optional
import generated

from smoke.CalculationResult import CalculationResult

@_mark_callback_base
class ListenerWithProperties(generated.smoke_ListenerWithProperties):
    @classmethod
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        _install_callback_adapters(cls, __class__, [
            ("message", "__gluecodium_callback_736d6f6b652e4c697374656e65725769746850726f706572746965732e6d657373616765_get", "get", "get_message",
             lambda: ([], str)),
            ("message", "__gluecodium_callback_736d6f6b652e4c697374656e65725769746850726f706572746965732e6d657373616765_set", "set", "set_message",
             lambda: ([str], None)),
            ("packed_message", "__gluecodium_callback_736d6f6b652e4c697374656e65725769746850726f706572746965732e7061636b65644d657373616765_get", "get", "get_packed_message",
             lambda: ([], CalculationResult)),
            ("packed_message", "__gluecodium_callback_736d6f6b652e4c697374656e65725769746850726f706572746965732e7061636b65644d657373616765_set", "set", "set_packed_message",
             lambda: ([CalculationResult], None)),
            ("structured_message", "__gluecodium_callback_736d6f6b652e4c697374656e65725769746850726f706572746965732e737472756374757265644d657373616765_get", "get", "get_structured_message",
             lambda: ([], ListenerWithProperties.ResultStruct)),
            ("structured_message", "__gluecodium_callback_736d6f6b652e4c697374656e65725769746850726f706572746965732e737472756374757265644d657373616765_set", "set", "set_structured_message",
             lambda: ([ListenerWithProperties.ResultStruct], None)),
            ("enumerated_message", "__gluecodium_callback_736d6f6b652e4c697374656e65725769746850726f706572746965732e656e756d6572617465644d657373616765_get", "get", "get_enumerated_message",
             lambda: ([], ListenerWithProperties.ResultEnum)),
            ("enumerated_message", "__gluecodium_callback_736d6f6b652e4c697374656e65725769746850726f706572746965732e656e756d6572617465644d657373616765_set", "set", "set_enumerated_message",
             lambda: ([ListenerWithProperties.ResultEnum], None)),
            ("arrayed_message", "__gluecodium_callback_736d6f6b652e4c697374656e65725769746850726f706572746965732e617272617965644d657373616765_get", "get", "get_arrayed_message",
             lambda: ([], list[str])),
            ("arrayed_message", "__gluecodium_callback_736d6f6b652e4c697374656e65725769746850726f706572746965732e617272617965644d657373616765_set", "set", "set_arrayed_message",
             lambda: ([list[str]], None)),
            ("mapped_message", "__gluecodium_callback_736d6f6b652e4c697374656e65725769746850726f706572746965732e6d61707065644d657373616765_get", "get", "get_mapped_message",
             lambda: ([], dict[str, float])),
            ("mapped_message", "__gluecodium_callback_736d6f6b652e4c697374656e65725769746850726f706572746965732e6d61707065644d657373616765_set", "set", "set_mapped_message",
             lambda: ([dict[str, float]], None)),
            ("buffered_message", "__gluecodium_callback_736d6f6b652e4c697374656e65725769746850726f706572746965732e62756666657265644d657373616765_get", "get", "get_buffered_message",
             lambda: ([], bytes)),
            ("buffered_message", "__gluecodium_callback_736d6f6b652e4c697374656e65725769746850726f706572746965732e62756666657265644d657373616765_set", "set", "set_buffered_message",
             lambda: ([bytes], None)),
        ])
    def __init__(self, native=None):
        # Subclass the native pybind11 type so that a Python override of an interface
        # method is dispatched through the generated trampoline. When `native` is an
        # existing native instance (returned by a factory), adopt it via the generated
        # adoption constructor and retain the original native object for calls back into
        # C++; otherwise construct a fresh trampoline.
        if native is not None and isinstance(native, generated.smoke_ListenerWithProperties):
            super().__init__(native)
            self._native = native
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
            if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_ListenerWithProperties.ResultStruct):
                super().__init__(args[0])
            else:
                super().__init__(generated.smoke_ListenerWithProperties.ResultStruct(
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
    
        NONE = generated.smoke_ListenerWithProperties.ResultEnum.NONE
        RESULT = generated.smoke_ListenerWithProperties.ResultEnum.RESULT
    
        @property
        def _native(self):
            return self.value
    
    
    
    StringToDouble = dict[str, float]
    
    

