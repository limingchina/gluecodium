

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase
from enum import Enum
from typing import Optional
from typing import Callable
import generated


class ExcludedComments(_NativeBase):
    """This is some very useful class."""
    def __init__(self, native):
        super().__init__(native)

    def some_method_with_all_comments(self, input_parameter: str) -> bool:
        """This is some very useful method that measures the usefulness of its input."""
        return _wrap(self._native.some_method_with_all_comments(_unwrap(input_parameter, str)), bool)

    def some_method_without_return_type_or_input_parameters(self):
        """This is some very useful method that does nothing."""
        return _wrap(self._native.some_method_without_return_type_or_input_parameters(), None)

    @property
    def is_some_property(self) -> bool:
        """Some very useful property."""
        return _wrap(self._native.is_some_property, bool)

    @is_some_property.setter
    def is_some_property(self, value: bool):
        """Sets some very useful property."""
        self._native.is_some_property = _unwrap(value, bool)

    class SomeStruct(_NativeBase):
        """This is some very useful struct."""
        def __init__(self, *args, **kwargs):
            if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_ExcludedComments.SomeStruct):
                super().__init__(args[0])
            else:
                super().__init__(generated.smoke_ExcludedComments.SomeStruct(
                    *[_unwrap(arg) for arg in args],
                    **{k: _unwrap(v) for k, v in kwargs.items()}
                ))
    
        @property
        def some_field(self) -> bool:
            """How useful this struct is
    remains to be seen"""
            return _wrap(self._native.some_field, bool)
        @some_field.setter
        def some_field(self, value: bool):
          self._native.some_field = _unwrap(value, bool)
    
    
    
    
    class SomeEnum(Enum):
        """This is some very useful enum."""
    
        USELESS = generated.smoke_ExcludedComments.SomeEnum.USELESS
    
        @property
        def _native(self):
            return self.value
    
    
    
    class SomethingWrongError(Exception):
        """This is some very useful exception."""
    
        def __init__(self, message: str):
            super().__init__(message)
            self.message = message
    
    
    
    #: This is some very useful typealias.
    Usefulness = bool
    
    
    
    #: This is some very useful lambda that does it.
    SomeLambda = Callable[[str, int], float]
    
    

    #: This is some very useful constant.
    VERY_USEFUL = True

