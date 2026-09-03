

from smoke.EnumOptionSet import EnumOptionSet
from enum import Enum
import typing

class UseEnumOptionSet:

    set_field: set[EnumOptionSet]

    set_field_empty: set[EnumOptionSet]

    set_field_value: set[EnumOptionSet]

    @staticmethod
    def round_trip(input: set[EnumOptionSet]) -> set[EnumOptionSet]:
        ...


