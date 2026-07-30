

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper
from typing import Optional



import generated


class CommentsInterface(generated.smoke_CommentsInterface):
    """This is some very useful interface."""
    def __init__(self, native=None):
        # Subclass the native pybind11 type so that a Python override of an interface
        # method is dispatched through the generated trampoline. When `native` is an
        # existing native instance (returned by a factory), adopt it via the generated
        # adoption constructor; otherwise construct a fresh trampoline. `self._native`
        # aliases the wrapper itself so the rest of the generated code can reach the
        # native object uniformly (e.g. when passing this interface back into a C++
        # call site).
        if native is not None and isinstance(native, generated.smoke_CommentsInterface):
            super().__init__(native)
        else:
            super().__init__()
        self._native = self

    def some_method_with_all_comments(self, input: str) -> bool:
        """This is some very useful method that measures the usefulness of its input."""
        return _wrap(generated.smoke_CommentsInterface.some_method_with_all_comments(self, _unwrap(input, str)), bool)

    def some_method_with_input_comments(self, input: str) -> bool:
        """This is some very useful method that measures the usefulness of its input."""
        return _wrap(generated.smoke_CommentsInterface.some_method_with_input_comments(self, _unwrap(input, str)), bool)

    def some_method_with_output_comments(self, input: str) -> bool:
        """This is some very useful method that measures the usefulness of its input."""
        return _wrap(generated.smoke_CommentsInterface.some_method_with_output_comments(self, _unwrap(input, str)), bool)

    def some_method_with_no_comments(self, input: str) -> bool:
        """This is some very useful method that measures the usefulness of its input."""
        return _wrap(generated.smoke_CommentsInterface.some_method_with_no_comments(self, _unwrap(input, str)), bool)

    def some_method_without_return_type_with_all_comments(self, input: str):
        """This is some very useful method that does not measure the usefulness of its input."""
        return _wrap(generated.smoke_CommentsInterface.some_method_without_return_type_with_all_comments(self, _unwrap(input, str)), None)

    def some_method_without_return_type_with_no_comments(self, input: str):
        """This is some very useful method that does not measure the usefulness of its input."""
        return _wrap(generated.smoke_CommentsInterface.some_method_without_return_type_with_no_comments(self, _unwrap(input, str)), None)

    def some_method_without_input_parameters_with_all_comments(self) -> bool:
        """This is some very useful method that measures the usefulness of something."""
        return _wrap(generated.smoke_CommentsInterface.some_method_without_input_parameters_with_all_comments(self), bool)

    def some_method_without_input_parameters_with_no_comments(self) -> bool:
        """This is some very useful method that measures the usefulness of something."""
        return _wrap(generated.smoke_CommentsInterface.some_method_without_input_parameters_with_no_comments(self), bool)

    def some_method_with_nothing(self):
        return _wrap(generated.smoke_CommentsInterface.some_method_with_nothing(self), None)

    def some_method_without_return_type_or_input_parameters(self):
        """This is some very useful method that does nothing."""
        return _wrap(generated.smoke_CommentsInterface.some_method_without_return_type_or_input_parameters(self), None)

    @property
    def is_some_property(self) -> bool:
        """Some very useful property."""
        return _wrap(generated.smoke_CommentsInterface.is_some_property.fget(self), bool)

    @is_some_property.setter
    def is_some_property(self, value: bool):
        """Sets some very useful property."""
        generated.smoke_CommentsInterface.is_some_property.fset(self, _unwrap(value, bool))

    #: This is some very useful constant.
    VERY_USEFUL = True

