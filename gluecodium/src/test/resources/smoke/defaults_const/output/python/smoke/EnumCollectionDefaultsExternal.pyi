

from fire.ExternalEnum1 import ExternalEnum1
from fire.ExternalEnum2 import ExternalEnum2
from fire.ExternalEnum3 import ExternalEnum3
from fire.ExternalEnum4 import ExternalEnum4
import typing

class EnumCollectionDefaultsExternal:

    list_field: list[ExternalEnum1]

    set_field: set[ExternalEnum2]

    map_field: dict[ExternalEnum3, ExternalEnum4]

