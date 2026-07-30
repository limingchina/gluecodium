

import typing

class SimpleInterface:

    def get_string_value(self) -> str:
        ...

    def use_simple_interface(self, input: SimpleInterface) -> SimpleInterface:
        ...

