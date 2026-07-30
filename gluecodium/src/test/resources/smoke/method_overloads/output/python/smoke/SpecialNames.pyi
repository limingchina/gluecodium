

import typing

class SpecialNames:

    def create(self):
        ...

    def release(self):
        ...

    def create_proxy(self):
        ...

    def _uppercase(self):
        ...

    @staticmethod
    def make(result: str) -> SpecialNames:
        ...

