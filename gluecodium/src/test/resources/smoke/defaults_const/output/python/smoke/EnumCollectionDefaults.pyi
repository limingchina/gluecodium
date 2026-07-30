

from fire.Enum1 import Enum1
from fire.Enum2 import Enum2
from fire.Enum3 import Enum3
from fire.Enum4 import Enum4
import typing

class EnumCollectionDefaults:

    list_field: list[Enum1]

    set_field: set[Enum2]

    map_field: dict[Enum3, Enum4]

