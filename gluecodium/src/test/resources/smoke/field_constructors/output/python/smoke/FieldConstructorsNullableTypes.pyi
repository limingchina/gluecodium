

from enum import Enum
import typing
from typing import Optional

class FieldConstructorsNullableTypes:
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, nullable_field: Optional[FieldConstructorsNullableTypes.StructWithParameters]) -> None: ...

    nullable_field: Optional[FieldConstructorsNullableTypes.StructWithParameters]

    class StructWithParameters:
        @typing.overload
        def __init__(self) -> None: ...
        @typing.overload
        def __init__(self, food_type: FieldConstructorsNullableTypes.FoodType) -> None: ...

        food_type: FieldConstructorsNullableTypes.FoodType



    class FoodType(Enum):

        VEGETABLES = 0
        FRUITS = 1
