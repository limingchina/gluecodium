

from smoke.PI import PI

class AttributesWithComments:
    """Class comment"""

    def __init__(self, native):
        self._native = native

    Function comment
    def very_fun(self):
        """Function comment"""
        return self._native.very_fun()

    Property comment
    @property
    def prop(self) -> str:
        """Property comment"""
        return self._native.prop


