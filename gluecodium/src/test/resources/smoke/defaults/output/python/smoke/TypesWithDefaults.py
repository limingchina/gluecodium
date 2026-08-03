

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase
from enum import Enum
from typing import Optional
import generated


class TypesWithDefaults(_NativeBase):
    def __init__(self, *args, **kwargs):
        if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_TypesWithDefaults):
            super().__init__(args[0])
        else:
            super().__init__(generated.smoke_TypesWithDefaults(
                *[_unwrap(arg) for arg in args],
                **{k: _unwrap(v) for k, v in kwargs.items()}
            ))

    class StructWithDefaults(_NativeBase):
        def __init__(self, *args, **kwargs):
            if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_TypesWithDefaults.StructWithDefaults):
                super().__init__(args[0])
            else:
                super().__init__(generated.smoke_TypesWithDefaults.StructWithDefaults(
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
    
    
    
    
    class ImmutableStructWithDefaults(_NativeBase):
        def __init__(self, *args, **kwargs):
            if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_TypesWithDefaults.ImmutableStructWithDefaults):
                super().__init__(args[0])
            else:
                super().__init__(generated.smoke_TypesWithDefaults.ImmutableStructWithDefaults(
                    *[_unwrap(arg) for arg in args],
                    **{k: _unwrap(v) for k, v in kwargs.items()}
                ))
    
        @property
        def int_field(self) -> int:
            return _wrap(self._native.int_field, int)
    
    
        @property
        def uint_field(self) -> int:
            return _wrap(self._native.uint_field, int)
    
    
        @property
        def float_field(self) -> float:
            return _wrap(self._native.float_field, float)
    
    
        @property
        def double_field(self) -> float:
            return _wrap(self._native.double_field, float)
    
    
        @property
        def bool_field(self) -> bool:
            return _wrap(self._native.bool_field, bool)
    
    
        @property
        def string_field(self) -> str:
            return _wrap(self._native.string_field, str)
    
    
    
    
    class ImmutableStructWithCollections(_NativeBase):
        def __init__(self, *args, **kwargs):
            if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_TypesWithDefaults.ImmutableStructWithCollections):
                super().__init__(args[0])
            else:
                super().__init__(generated.smoke_TypesWithDefaults.ImmutableStructWithCollections(
                    *[_unwrap(arg) for arg in args],
                    **{k: _unwrap(v) for k, v in kwargs.items()}
                ))
    
        @property
        def nullable_list_field(self):
            return _wrap(self._native.nullable_list_field, Optional[list[int]])
    
    
        @property
        def empty_list_field(self) -> list[int]:
            return _wrap(self._native.empty_list_field, list[int])
    
    
        @property
        def values_list_field(self) -> list[int]:
            return _wrap(self._native.values_list_field, list[int])
    
    
        @property
        def nullable_map_field(self):
            return _wrap(self._native.nullable_map_field, Optional[dict[int, str]])
    
    
        @property
        def empty_map_field(self) -> dict[int, str]:
            return _wrap(self._native.empty_map_field, dict[int, str])
    
    
        @property
        def values_map_field(self) -> dict[int, str]:
            return _wrap(self._native.values_map_field, dict[int, str])
    
    
        @property
        def nullable_set_field(self):
            return _wrap(self._native.nullable_set_field, Optional[set[str]])
    
    
        @property
        def empty_set_field(self) -> set[str]:
            return _wrap(self._native.empty_set_field, set[str])
    
    
        @property
        def values_set_field(self) -> set[str]:
            return _wrap(self._native.values_set_field, set[str])
    
    
    
    
    class ImmutableStructWithFieldConstructorAndCollections(_NativeBase):
        def __init__(self, *args, **kwargs):
            if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_TypesWithDefaults.ImmutableStructWithFieldConstructorAndCollections):
                super().__init__(args[0])
            else:
                super().__init__(generated.smoke_TypesWithDefaults.ImmutableStructWithFieldConstructorAndCollections(
                    *[_unwrap(arg) for arg in args],
                    **{k: _unwrap(v) for k, v in kwargs.items()}
                ))
    
        @property
        def nullable_list_field(self):
            return _wrap(self._native.nullable_list_field, Optional[list[int]])
    
    
        @property
        def empty_list_field(self) -> list[int]:
            return _wrap(self._native.empty_list_field, list[int])
    
    
        @property
        def values_list_field(self) -> list[int]:
            return _wrap(self._native.values_list_field, list[int])
    
    
        @property
        def nullable_map_field(self):
            return _wrap(self._native.nullable_map_field, Optional[dict[int, str]])
    
    
        @property
        def empty_map_field(self) -> dict[int, str]:
            return _wrap(self._native.empty_map_field, dict[int, str])
    
    
        @property
        def values_map_field(self) -> dict[int, str]:
            return _wrap(self._native.values_map_field, dict[int, str])
    
    
        @property
        def nullable_set_field(self):
            return _wrap(self._native.nullable_set_field, Optional[set[str]])
    
    
        @property
        def empty_set_field(self) -> set[str]:
            return _wrap(self._native.empty_set_field, set[str])
    
    
        @property
        def values_set_field(self) -> set[str]:
            return _wrap(self._native.values_set_field, set[str])
    
    
        @property
        def some_field(self) -> int:
            return _wrap(self._native.some_field, int)
    
    
        @property
        def another_field(self) -> int:
            return _wrap(self._native.another_field, int)
    
    
    
    
    class SomeImmutableStructWithDefaults(_NativeBase):
        def __init__(self, *args, **kwargs):
            if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_TypesWithDefaults.SomeImmutableStructWithDefaults):
                super().__init__(args[0])
            else:
                super().__init__(generated.smoke_TypesWithDefaults.SomeImmutableStructWithDefaults(
                    *[_unwrap(arg) for arg in args],
                    **{k: _unwrap(v) for k, v in kwargs.items()}
                ))
    
        @property
        def int_field(self) -> int:
            return _wrap(self._native.int_field, int)
    
    
    
    
    class ImmutableStructWithFieldUsingImmutableStruct(_NativeBase):
        def __init__(self, *args, **kwargs):
            if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_TypesWithDefaults.ImmutableStructWithFieldUsingImmutableStruct):
                super().__init__(args[0])
            else:
                super().__init__(generated.smoke_TypesWithDefaults.ImmutableStructWithFieldUsingImmutableStruct(
                    *[_unwrap(arg) for arg in args],
                    **{k: _unwrap(v) for k, v in kwargs.items()}
                ))
    
        @property
        def some_field1(self) -> TypesWithDefaults.SomeImmutableStructWithDefaults:
            return _wrap(self._native.some_field1, TypesWithDefaults.SomeImmutableStructWithDefaults)
    
    
        @property
        def some_field2(self) -> TypesWithDefaults.ImmutableStructWithCollections:
            return _wrap(self._native.some_field2, TypesWithDefaults.ImmutableStructWithCollections)
    
    
    
    
    class ImmutableStructWithFieldConstructorAndFieldUsingImmutableStruct(_NativeBase):
        def __init__(self, *args, **kwargs):
            if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_TypesWithDefaults.ImmutableStructWithFieldConstructorAndFieldUsingImmutableStruct):
                super().__init__(args[0])
            else:
                super().__init__(generated.smoke_TypesWithDefaults.ImmutableStructWithFieldConstructorAndFieldUsingImmutableStruct(
                    *[_unwrap(arg) for arg in args],
                    **{k: _unwrap(v) for k, v in kwargs.items()}
                ))
    
        @property
        def some_field1(self) -> TypesWithDefaults.SomeImmutableStructWithDefaults:
            return _wrap(self._native.some_field1, TypesWithDefaults.SomeImmutableStructWithDefaults)
    
    
        @property
        def some_field2(self) -> TypesWithDefaults.ImmutableStructWithCollections:
            return _wrap(self._native.some_field2, TypesWithDefaults.ImmutableStructWithCollections)
    
    
        @property
        def some_field(self) -> int:
            return _wrap(self._native.some_field, int)
    
    
        @property
        def another_field(self) -> int:
            return _wrap(self._native.another_field, int)
    
    
    
    
    class ImmutableStructWithNullableFieldUsingImmutableStruct(_NativeBase):
        def __init__(self, *args, **kwargs):
            if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_TypesWithDefaults.ImmutableStructWithNullableFieldUsingImmutableStruct):
                super().__init__(args[0])
            else:
                super().__init__(generated.smoke_TypesWithDefaults.ImmutableStructWithNullableFieldUsingImmutableStruct(
                    *[_unwrap(arg) for arg in args],
                    **{k: _unwrap(v) for k, v in kwargs.items()}
                ))
    
        @property
        def some_field1(self):
            return _wrap(self._native.some_field1, Optional[TypesWithDefaults.SomeImmutableStructWithDefaults])
    
    
        @property
        def some_field2(self):
            return _wrap(self._native.some_field2, Optional[TypesWithDefaults.ImmutableStructWithCollections])
    
    
    
    
    class ImmutableStructWithFieldConstructorAndNullableFieldUsingImmutableStruct(_NativeBase):
        def __init__(self, *args, **kwargs):
            if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_TypesWithDefaults.ImmutableStructWithFieldConstructorAndNullableFieldUsingImmutableStruct):
                super().__init__(args[0])
            else:
                super().__init__(generated.smoke_TypesWithDefaults.ImmutableStructWithFieldConstructorAndNullableFieldUsingImmutableStruct(
                    *[_unwrap(arg) for arg in args],
                    **{k: _unwrap(v) for k, v in kwargs.items()}
                ))
    
        @property
        def some_field1(self):
            return _wrap(self._native.some_field1, Optional[TypesWithDefaults.SomeImmutableStructWithDefaults])
    
    
        @property
        def some_field2(self):
            return _wrap(self._native.some_field2, Optional[TypesWithDefaults.ImmutableStructWithCollections])
    
    
        @property
        def some_field(self) -> int:
            return _wrap(self._native.some_field, int)
    
    
        @property
        def another_field(self) -> int:
            return _wrap(self._native.another_field, int)
    
    
    

