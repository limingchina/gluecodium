

from smoke._DartInternalClassWithInternalTypedef import _DartInternalClassWithInternalTypedef
from enum import Enum
import typing

class SomeDartClassThatUsesInternal:

    def _add_entity(self, entity: _DartInternalClassWithInternalTypedef):
        """"""
        ...

    _ListOfInternals = list[_DartInternalClassWithInternalTypedef]
    
    

