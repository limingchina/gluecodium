

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase
from enum import Enum
from typing import Optional
import generated


class PlatformComments(_NativeBase):
    def __init__(self, native):
        super().__init__(native)

    def do_nothing(self):
        """This is some very useless method that ."""
        return _wrap(self._native.do_nothing(), None)

    def do_magic(self):
        return _wrap(self._native.do_magic(), None)

    def some_method_with_all_comments(self, input: str) -> bool:
        """This is some very useful method that measures the usefulness of its input or \esc@pe{s}."""
        return _wrap(self._native.some_method_with_all_comments(_unwrap(input, str)), bool)

    def some_deprecated_method(self):
        """"""
        return _wrap(self._native.some_deprecated_method(), None)

    class Something(_NativeBase):
        """This is a."""
        def __init__(self, *args, **kwargs):
            if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_PlatformCommentssomething):
                super().__init__(args[0])
            else:
                super().__init__(generated.smoke_PlatformCommentssomething(
                    *[_unwrap(arg) for arg in args],
                    **{k: _unwrap(v) for k, v in kwargs.items()}
                ))
    
        @property
        def nothing(self) -> str:
            return _wrap(self._native.nothing, str)
        @nothing.setter
        def nothing(self, value: str):
          self._native.nothing = _unwrap(value, str)
    
    
    
    
    class SomeEnum(Enum):
    
        USELESS = 0
        USEFUL = 1
    
    
    
    class SomethingWrongError(Exception):
        """An  when something goes wrong."""
    
        def __init__(self, message: str):
            super().__init__(message)
            self.message = message
    
    

