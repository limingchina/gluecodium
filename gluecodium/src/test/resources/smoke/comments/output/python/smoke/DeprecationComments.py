

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase
from enum import Enum
from typing import Optional
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

    class SomeStruct(_NativeBase):
        """This is some very useful struct."""
        def __init__(self, *args, **kwargs):
            if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_DeprecationCommentsSomeStruct):
                super().__init__(args[0])
            else:
                super().__init__(generated.smoke_DeprecationCommentsSomeStruct(
                    *[_unwrap(arg) for arg in args],
                    **{k: _unwrap(v) for k, v in kwargs.items()}
                ))
    
        @property
        def some_field(self) -> bool:
            """How useful this struct is."""
            return _wrap(self._native.some_field, bool)
        @some_field.setter
        def some_field(self, value: bool):
          self._native.some_field = _unwrap(value, bool)
    
    
    
    
    class SomeEnum(Enum):
        """This is some very useful enum."""
    
        USELESS = 0
    
    
    
    #: This is some very useful typedef.
    bool = bool
    
    
    
    class SomethingWrongError(Exception):
        """"""
    
        def __init__(self, message: str):
            super().__init__(message)
            self.message = message
    
    

