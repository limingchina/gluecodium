

from smoke.SomethingEnum import SomethingEnum
import typing

class StructWithPosEnums:

    first_field: SomethingEnum

    explicit_field: SomethingEnum

    last_field: SomethingEnum

    FIRST_CONSTANT = SomethingEnum.REALLY_FIRST

