

from enum import Enum
import typing
from typing import Optional

class TypeCollection:

    class Point:

        x: float

        y: float



    class StructHavingAliasFieldDefinedBelow:

        field: int



    PointTypeDef = Point



    StorageId = int



    INVALID_STORAGE_ID = 0
