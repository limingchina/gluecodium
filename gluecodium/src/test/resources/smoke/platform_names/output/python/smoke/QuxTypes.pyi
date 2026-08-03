

from enum import Enum
import typing

class QuxTypes:

    class QuxStruct:
    
        qux_field: str
    
        @staticmethod
        def qux_make(qux_parameter: str) -> QuxTypes.QuxStruct:
            ...
    
    
    
    class QuxEnum(Enum):
    
        QUX_ITEM = 0
    
    
    
    QuxTypedef = float
    
    

