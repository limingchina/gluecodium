

from smoke.SomeEnum import SomeEnum
from smoke.SomethingWrongError import SomethingWrongError


from _native_base import _NativeBase

import generated


class PlatformComments(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    This is some very useless method that {@Cpp does nothing}{@Kotlin makes some tea}{@Java makes some coffee}{@Swift is very swift}{@Dart cannot have overloads}.
    def do_nothing(self):
        """This is some very useless method that {@Cpp does nothing}{@Kotlin makes some tea}{@Java makes some coffee}{@Swift is very swift}{@Dart cannot have overloads}."""
        return self._native.do_nothing()

    {@Cpp Cooks very special C++ sauce.}{@Java Makes some coffee.}{@Kotlin Makes some tea.}{@Swift Eats a hip bruschetta.}{@Dart Colors everything in fuchsia.}
    def do_magic(self):
        """{@Cpp Cooks very special C++ sauce.}{@Java Makes some coffee.}{@Kotlin Makes some tea.}{@Swift Eats a hip bruschetta.}{@Dart Colors everything in fuchsia.}"""
        return self._native.do_magic()

    This is some very useful method that measures the usefulness of its input or \\esc\@pe\{s\}.
    def some_method_with_all_comments(self, input: str) -> bool:
        """This is some very useful method that measures the usefulness of its input or \\esc\@pe\{s\}."""
        return self._native.some_method_with_all_comments(input)


    def some_deprecated_method(self):
        """"""
        return self._native.some_deprecated_method()

from enum import Enum


class SomeEnum(Enum):
    """"""

    USELESS = 0
    USEFUL = 1

