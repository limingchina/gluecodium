

from smoke.SomethingEnum import SomethingEnum
from enum import Enum
import typing

class StructWithPosEnums:

    first_field: SomethingEnum

    explicit_field: SomethingEnum

    last_field: SomethingEnum

    FIRST_CONSTANT = SomethingEnum.REALLY_FIRST


