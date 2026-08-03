

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase
from enum import Enum
from typing import Optional
from typing import Callable
import generated


class Comments(_NativeBase):
    """This is some very useful ."""
    def __init__(self, native):
        super().__init__(native)

    def some_method_with_all_comments(self, input_parameter: str) -> bool:
        """This is some very useful method that measures the usefulness of its input."""
        return _wrap(self._native.some_method_with_all_comments(_unwrap(input_parameter, str)), bool)

    def some_method_with_input_comments(self, input: str) -> bool:
        """This is some very useful method that measures the usefulness of its input."""
        return _wrap(self._native.some_method_with_input_comments(_unwrap(input, str)), bool)

    def some_method_with_output_comments(self, input: str) -> bool:
        """This is some very useful method that measures the usefulness of its input."""
        return _wrap(self._native.some_method_with_output_comments(_unwrap(input, str)), bool)

    def some_method_with_no_comments(self, input: str) -> bool:
        """This is some very useful method that measures the usefulness of its input."""
        return _wrap(self._native.some_method_with_no_comments(_unwrap(input, str)), bool)

    def some_method_without_return_type_with_all_comments(self, input: str):
        """This is some very useful method that does not measure the usefulness of its input."""
        return _wrap(self._native.some_method_without_return_type_with_all_comments(_unwrap(input, str)), None)

    def some_method_without_return_type_with_no_comments(self, input: str):
        """This is some very useful method that does not measure the usefulness of its input."""
        return _wrap(self._native.some_method_without_return_type_with_no_comments(_unwrap(input, str)), None)

    def some_method_without_input_parameters_with_all_comments(self) -> bool:
        """This is some very useful method that measures the usefulness of something."""
        return _wrap(self._native.some_method_without_input_parameters_with_all_comments(), bool)

    def some_method_without_input_parameters_with_no_comments(self) -> bool:
        """This is some very useful method that measures the usefulness of something."""
        return _wrap(self._native.some_method_without_input_parameters_with_no_comments(), bool)

    def some_method_with_nothing(self):
        return _wrap(self._native.some_method_with_nothing(), None)

    def some_method_without_return_type_or_input_parameters(self):
        """This is some very useful method that does nothing."""
        return _wrap(self._native.some_method_without_return_type_or_input_parameters(), None)

    def one_parameter_comment_only(self, undocumented: str, documented: str) -> str:
        """"""
        return _wrap(self._native.one_parameter_comment_only(_unwrap(undocumented, str), _unwrap(documented, str)), str)

    def return_comment_only(self, undocumented: str) -> str:
        """"""
        return _wrap(self._native.return_comment_only(_unwrap(undocumented, str)), str)

    @property
    def is_some_property(self) -> bool:
        """Some very useful property."""
        return _wrap(self._native.is_some_property, bool)

    @is_some_property.setter
    def is_some_property(self, value: bool):
        """Sets some very useful property."""
        self._native.is_some_property = _unwrap(value, bool)

    @property
    def only_getter_property(self) -> int:
        """OnlyGetterProperty, which does not have a setter."""
        return _wrap(self._native.only_getter_property, int)


    @property
    def is_is_visible(self) -> bool:
        """A flag that determines if [OnlyGetterProperty] is visible on the screen."""
        return _wrap(self._native.is_is_visible, bool)

    @is_is_visible.setter
    def is_is_visible(self, value: bool):
        """Sets the visibility flag that controls if [OnlyGetterProperty] should be visible on the screen."""
        self._native.is_is_visible = _unwrap(value, bool)

    class SomeStruct(_NativeBase):
        """This is some very useful struct."""
        def __init__(self, *args, **kwargs):
            if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_Comments.SomeStruct):
                super().__init__(args[0])
            else:
                super().__init__(generated.smoke_Comments.SomeStruct(
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
    
    
        @property
        def nullable_field(self):
            """Can be `None`"""
            return _wrap(self._native.nullable_field, Optional[str])
        @nullable_field.setter
        def nullable_field(self, value):
          self._native.nullable_field = _unwrap(value, Optional[str])
    
    
        def some_struct_method(self):
            """This is some struct method that does nothing."""
            return _wrap(self._native.some_struct_method(), None)
    
        @staticmethod
        def some_static_struct_method():
            """This is some static struct method that does nothing."""
            generated.smoke_Comments.SomeStruct.some_static_struct_method()
    
    
    
    class SomeEnum(Enum):
        """This is some very useful enum."""
    
        USELESS = generated.smoke_Comments.SomeEnum.USELESS
        USEFUL = generated.smoke_Comments.SomeEnum.USEFUL
    
        @property
        def _native(self):
            return self.value
    
    
    
    class SomethingWrongError(Exception):
        """This is some very useful exception."""
    
        def __init__(self, message: str):
            super().__init__(message)
            self.message = message
    
    
    
    #: This is some very useful typedef.
    Usefulness = bool
    
    
    
    #: This is some very useful lambda that does it.
    SomeLambda = Callable[[str, int], float]
    
    

    #: This is some very useful constant.
    VERY_USEFUL = True

