

from enum import Enum
import typing
from typing import Callable

class SpecialNamesInterface:

    def dispatch(self, callback: Callable[[], None]):
        ...

    Callback = Callable[[], None]
    
    

