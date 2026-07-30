

from namerules.NameRulesExample import NameRulesExample
from namerules.NameRulesExampleErrorCode import NameRulesExampleErrorCode
from namerules.NameRulesExampleStruct import NameRulesExampleStruct
import typing

class NameRules:

    @staticmethod
    def create() -> NameRules:
        ...

    def some_method(self, some_argument: NameRulesExampleStruct) -> float:
        ...

    @property
    def int_property(self) -> int:
        ...

    @int_property.setter
    def int_property(self, value: int) -> None:
        ...

    @property
    def is_boolean_property(self) -> bool:
        ...

    @is_boolean_property.setter
    def is_boolean_property(self, value: bool) -> None:
        ...

    @property
    def struct_property(self) -> NameRulesExampleStruct:
        ...

    @struct_property.setter
    def struct_property(self, value: NameRulesExampleStruct) -> None:
        ...

