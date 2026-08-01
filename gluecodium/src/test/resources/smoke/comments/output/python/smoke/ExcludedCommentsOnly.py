

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase
from enum import Enum
from typing import Optional
from typing import Callable
import generated


class ExcludedCommentsOnly(_NativeBase):
    """"""
    def __init__(self, native):
        super().__init__(native)

    def some_method_with_all_comments(self, input_parameter: str) -> bool:
        """"""
        return _wrap(self._native.some_method_with_all_comments(_unwrap(input_parameter, str)), bool)

    def some_method_without_return_type_or_input_parameters(self):
        """"""
        return _wrap(self._native.some_method_without_return_type_or_input_parameters(), None)

    @property
    def is_some_property(self) -> bool:
        """"""
        return _wrap(self._native.is_some_property, bool)

    @is_some_property.setter
    def is_some_property(self, value: bool):
        self._native.is_some_property = _unwrap(value, bool)

    #: 
    VERY_USEFUL = True

    class SomeStruct(_NativeBase):
        """"""
        def __init__(self, *args, **kwargs):
            if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_ExcludedCommentsOnlySomeStruct):
                super().__init__(args[0])
            else:
                super().__init__(generated.smoke_ExcludedCommentsOnlySomeStruct(
                    *[_unwrap(arg) for arg in args],
                    **{k: _unwrap(v) for k, v in kwargs.items()}
                ))
    
        @property
        def some_field(self) -> bool:
            """"""
            return _wrap(self._native.some_field, bool)
        @some_field.setter
        def some_field(self, value: bool):
          self._native.some_field = _unwrap(value, bool)
    
    
    
    
    class SomeEnum(Enum):
        """"""
    
        USELESS = 0
    
    
    
    #: 
    bool = bool
    
    
    
    #: 
    SomeLambda = Callable[[str, int], float]
    
    
    
    class SomethingWrongError(Exception):
        """"""
    
        def __init__(self, message: str):
            super().__init__(message)
            self.message = message
    
    

