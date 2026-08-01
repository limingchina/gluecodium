

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase
from enum import Enum
from typing import Optional
import generated


class DefaultValues(_NativeBase):
    def __init__(self, native):
        super().__init__(native)

    @staticmethod
    def process_struct_with_defaults(input: DefaultValues.StructWithDefaults) -> DefaultValues.StructWithDefaults:
        native_result = generated.smoke_DefaultValues.process_struct_with_defaults(_unwrap(input, DefaultValues.StructWithDefaults))
        return _get_or_create_wrapper(native_result, DefaultValues.StructWithDefaults)

    class StructWithDefaults(_NativeBase):
        def __init__(self, *args, **kwargs):
            if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_DefaultValuesStructWithDefaults):
                super().__init__(args[0])
            else:
                super().__init__(generated.smoke_DefaultValuesStructWithDefaults(
                    *[_unwrap(arg) for arg in args],
                    **{k: _unwrap(v) for k, v in kwargs.items()}
                ))
    
        @property
        def int_field(self) -> int:
            return _wrap(self._native.int_field, int)
        @int_field.setter
        def int_field(self, value: int):
          self._native.int_field = _unwrap(value, int)
    
    
        @property
        def uint_field(self) -> int:
            return _wrap(self._native.uint_field, int)
        @uint_field.setter
        def uint_field(self, value: int):
          self._native.uint_field = _unwrap(value, int)
    
    
        @property
        def float_field(self) -> float:
            return _wrap(self._native.float_field, float)
        @float_field.setter
        def float_field(self, value: float):
          self._native.float_field = _unwrap(value, float)
    
    
        @property
        def double_field(self) -> float:
            return _wrap(self._native.double_field, float)
        @double_field.setter
        def double_field(self, value: float):
          self._native.double_field = _unwrap(value, float)
    
    
        @property
        def bool_field(self) -> bool:
            return _wrap(self._native.bool_field, bool)
        @bool_field.setter
        def bool_field(self, value: bool):
          self._native.bool_field = _unwrap(value, bool)
    
    
        @property
        def string_field(self) -> str:
            return _wrap(self._native.string_field, str)
        @string_field.setter
        def string_field(self, value: str):
          self._native.string_field = _unwrap(value, str)
    
    
    
    
    class NullableStructWithDefaults(_NativeBase):
        def __init__(self, *args, **kwargs):
            if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_DefaultValuesNullableStructWithDefaults):
                super().__init__(args[0])
            else:
                super().__init__(generated.smoke_DefaultValuesNullableStructWithDefaults(
                    *[_unwrap(arg) for arg in args],
                    **{k: _unwrap(v) for k, v in kwargs.items()}
                ))
    
        @property
        def int_field(self):
            return _wrap(self._native.int_field, Optional[int])
        @int_field.setter
        def int_field(self, value):
          self._native.int_field = _unwrap(value, Optional[int])
    
    
        @property
        def uint_field(self):
            return _wrap(self._native.uint_field, Optional[int])
        @uint_field.setter
        def uint_field(self, value):
          self._native.uint_field = _unwrap(value, Optional[int])
    
    
        @property
        def float_field(self):
            return _wrap(self._native.float_field, Optional[float])
        @float_field.setter
        def float_field(self, value):
          self._native.float_field = _unwrap(value, Optional[float])
    
    
        @property
        def bool_field(self):
            return _wrap(self._native.bool_field, Optional[bool])
        @bool_field.setter
        def bool_field(self, value):
          self._native.bool_field = _unwrap(value, Optional[bool])
    
    
        @property
        def string_field(self):
            return _wrap(self._native.string_field, Optional[str])
        @string_field.setter
        def string_field(self, value):
          self._native.string_field = _unwrap(value, Optional[str])
    
    
    
    
    class StructWithSpecialDefaults(_NativeBase):
        def __init__(self, *args, **kwargs):
            if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_DefaultValuesStructWithSpecialDefaults):
                super().__init__(args[0])
            else:
                super().__init__(generated.smoke_DefaultValuesStructWithSpecialDefaults(
                    *[_unwrap(arg) for arg in args],
                    **{k: _unwrap(v) for k, v in kwargs.items()}
                ))
    
        @property
        def float_nan_field(self) -> float:
            return _wrap(self._native.float_nan_field, float)
        @float_nan_field.setter
        def float_nan_field(self, value: float):
          self._native.float_nan_field = _unwrap(value, float)
    
    
        @property
        def float_infinity_field(self) -> float:
            return _wrap(self._native.float_infinity_field, float)
        @float_infinity_field.setter
        def float_infinity_field(self, value: float):
          self._native.float_infinity_field = _unwrap(value, float)
    
    
        @property
        def float_negative_infinity_field(self) -> float:
            return _wrap(self._native.float_negative_infinity_field, float)
        @float_negative_infinity_field.setter
        def float_negative_infinity_field(self, value: float):
          self._native.float_negative_infinity_field = _unwrap(value, float)
    
    
        @property
        def double_nan_field(self) -> float:
            return _wrap(self._native.double_nan_field, float)
        @double_nan_field.setter
        def double_nan_field(self, value: float):
          self._native.double_nan_field = _unwrap(value, float)
    
    
        @property
        def double_infinity_field(self) -> float:
            return _wrap(self._native.double_infinity_field, float)
        @double_infinity_field.setter
        def double_infinity_field(self, value: float):
          self._native.double_infinity_field = _unwrap(value, float)
    
    
        @property
        def double_negative_infinity_field(self) -> float:
            return _wrap(self._native.double_negative_infinity_field, float)
        @double_negative_infinity_field.setter
        def double_negative_infinity_field(self, value: float):
          self._native.double_negative_infinity_field = _unwrap(value, float)
    
    
    
    
    class StructWithEmptyDefaults(_NativeBase):
        def __init__(self, *args, **kwargs):
            if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_DefaultValuesStructWithEmptyDefaults):
                super().__init__(args[0])
            else:
                super().__init__(generated.smoke_DefaultValuesStructWithEmptyDefaults(
                    *[_unwrap(arg) for arg in args],
                    **{k: _unwrap(v) for k, v in kwargs.items()}
                ))
    
        @property
        def ints_field(self) -> list[int]:
            return _wrap(self._native.ints_field, list[int])
        @ints_field.setter
        def ints_field(self, value: list[int]):
          self._native.ints_field = _unwrap(value, list[int])
    
    
        @property
        def floats_field(self) -> list[float]:
            return _wrap(self._native.floats_field, list[float])
        @floats_field.setter
        def floats_field(self, value: list[float]):
          self._native.floats_field = _unwrap(value, list[float])
    
    
        @property
        def map_field(self) -> dict[int, str]:
            return _wrap(self._native.map_field, dict[int, str])
        @map_field.setter
        def map_field(self, value: dict[int, str]):
          self._native.map_field = _unwrap(value, dict[int, str])
    
    
        @property
        def struct_field(self) -> DefaultValues.StructWithDefaults:
            return _wrap(self._native.struct_field, DefaultValues.StructWithDefaults)
        @struct_field.setter
        def struct_field(self, value: DefaultValues.StructWithDefaults):
          self._native.struct_field = _unwrap(value, DefaultValues.StructWithDefaults)
    
    
        @property
        def set_type_field(self) -> set[str]:
            return _wrap(self._native.set_type_field, set[str])
        @set_type_field.setter
        def set_type_field(self, value: set[str]):
          self._native.set_type_field = _unwrap(value, set[str])
    
    
    
    
    class StructWithTypedefDefaults(_NativeBase):
        def __init__(self, *args, **kwargs):
            if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_DefaultValuesStructWithTypedefDefaults):
                super().__init__(args[0])
            else:
                super().__init__(generated.smoke_DefaultValuesStructWithTypedefDefaults(
                    *[_unwrap(arg) for arg in args],
                    **{k: _unwrap(v) for k, v in kwargs.items()}
                ))
    
        @property
        def long_field(self) -> int:
            return _wrap(self._native.long_field, int)
        @long_field.setter
        def long_field(self, value: int):
          self._native.long_field = _unwrap(value, int)
    
    
        @property
        def bool_field(self) -> bool:
            return _wrap(self._native.bool_field, bool)
        @bool_field.setter
        def bool_field(self, value: bool):
          self._native.bool_field = _unwrap(value, bool)
    
    
        @property
        def string_field(self) -> str:
            return _wrap(self._native.string_field, str)
        @string_field.setter
        def string_field(self, value: str):
          self._native.string_field = _unwrap(value, str)
    
    
    
    
    int = int
    
    
    
    bool = bool
    
    
    
    str = str
    
    
    
    list[float] = list[float]
    
    
    
    dict[int, str] = dict[int, str]
    
    
    
    set[str] = set[str]
    
    

