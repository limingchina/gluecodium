

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper
from typing import Optional

from smoke.DeprecationCommentsSomeEnum import DeprecationCommentsSomeEnum


import generated


class DeprecationComments(generated.smoke_DeprecationComments):
    """This is some very useful interface."""
    def __init__(self, native=None):
        # Subclass the native pybind11 type so that a Python override of an interface
        # method is dispatched through the generated trampoline. When `native` is an
        # existing native instance (returned by a factory), adopt it via the generated
        # adoption constructor; otherwise construct a fresh trampoline. `self._native`
        # aliases the wrapper itself so the rest of the generated code can reach the
        # native object uniformly (e.g. when passing this interface back into a C++
        # call site).
        if native is not None and isinstance(native, generated.smoke_DeprecationComments):
            super().__init__(native)
        else:
            super().__init__()
        self._native = self

    def some_method_with_all_comments(self, input: str) -> bool:
        """This is some very useful method that measures the usefulness of its input."""
        return _wrap(generated.smoke_DeprecationComments.some_method_with_all_comments(self, _unwrap(input, str)), bool)

    @property
    def is_some_property(self) -> bool:
        """Some very useful property."""
        return _wrap(generated.smoke_DeprecationComments.is_some_property.fget(self), bool)

    @is_some_property.setter
    def is_some_property(self, value: bool):
        """Sets some very useful property."""
        generated.smoke_DeprecationComments.is_some_property.fset(self, _unwrap(value, bool))

    @property
    def property_but_not_accessors(self) -> str:
        """Describes the property but not accessors."""
        return _wrap(generated.smoke_DeprecationComments.property_but_not_accessors.fget(self), str)

    @property_but_not_accessors.setter
    def property_but_not_accessors(self, value: str):
        generated.smoke_DeprecationComments.property_but_not_accessors.fset(self, _unwrap(value, str))

    #: This is some very useful constant.
    VERY_USEFUL = True

