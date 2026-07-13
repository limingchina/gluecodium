

from smoke.DartInternalClassWithInternalTypedef import DartInternalClassWithInternalTypedef

class SomeDartClassThatUsesInternal:
    """"""

    def __init__(self, native):
        self._native = native


    def add_entity(self, entity: DartInternalClassWithInternalTypedef):
        """"""
        return self._native.add_entity(entity)

