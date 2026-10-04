

from smoke.SomethingEnum import SomethingEnum
from enum import Enum
import typing
from typing import Optional

class StructWithPosEnums:
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, first_field: SomethingEnum, explicit_field: SomethingEnum, last_field: SomethingEnum) -> None: ...

    first_field: SomethingEnum

    explicit_field: SomethingEnum

    last_field: SomethingEnum


    FIRST_CONSTANT = SomethingEnum.REALLY_FIRST
