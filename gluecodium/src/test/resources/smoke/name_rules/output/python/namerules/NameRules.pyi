

from namerules.NameRulesExample import NameRulesExample
from namerules.NameRulesExampleErrorCode import NameRulesExampleErrorCode
from namerules.NameRulesExampleStruct import NameRulesExampleStruct
import typing

from _native_base import _NativeBase

import generated


class NameRules(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    @staticmethod
    def create() -> NameRules: ...

    def some_method(self, some_argument: NameRulesExampleStruct) -> float: ...

    @property
    def int_property(self) -> int:
        """"""
        return _wrap(self._native.int_property, int)

    @int_property.setter
    def int_property(self, value: int):
        self._native.int_property = _unwrap(value, int)

    @property
    def is_boolean_property(self) -> bool:
        """"""
        return _wrap(self._native.is_boolean_property, bool)

    @is_boolean_property.setter
    def is_boolean_property(self, value: bool):
        self._native.is_boolean_property = _unwrap(value, bool)

    @property
    def struct_property(self) -> NameRulesExampleStruct:
        """"""
        return _wrap(self._native.struct_property, NameRulesExampleStruct)

    @struct_property.setter
    def struct_property(self, value: NameRulesExampleStruct):
        self._native.struct_property = _unwrap(value, NameRulesExampleStruct)

