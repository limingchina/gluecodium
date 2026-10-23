

from fire.SomeStruct import SomeStruct
from enum import Enum
import typing
from typing import Optional

class StructConstants:


    DUMMY = SomeStruct(42)

    DUMMY2 = SomeStruct(11)

    DUMMY3 = StructConstants.DUMMY2

    DUMMY4 = SomeStruct(-1)

    DUMMY4 = SomeStruct(-2)
