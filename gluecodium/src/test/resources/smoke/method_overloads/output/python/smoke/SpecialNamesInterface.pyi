

from smoke.SpecialNamesInterfaceCallback import SpecialNamesInterfaceCallback
import typing
from typing import Callable

class SpecialNamesInterface:

    def dispatch(self, callback: Callable[[], None]):
        ...

