

from enum import Enum
import typing

class FieldConstructorsNullableTypes:

    nullable_field: Optional[FieldConstructorsNullableTypes.StructWithParameters]

    class StructWithParameters:
    
        food_type: FieldConstructorsNullableTypes.FoodType
    
    
    
    class FoodType(Enum):
    
        VEGETABLES = 0
        FRUITS = 1
    
    

