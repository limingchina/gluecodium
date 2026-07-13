

from smoke.SomeEnum import SomeEnum
from smoke.SomethingWrongError import SomethingWrongError
from smoke.VERY_USEFUL import VERY_USEFUL
from smoke.bool import bool

from _native_base import _NativeBase


class ExcludedCommentsOnly(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    def some_method_with_all_comments(self, input_parameter: str) -> bool:
        """"""
        return self._native.some_method_with_all_comments(input_parameter)


    def some_method_without_return_type_or_input_parameters(self):
        """"""
        return self._native.some_method_without_return_type_or_input_parameters()


    @property
    def is_some_property(self) -> bool:
        """"""
        return self._native.is_some_property


