

import typing

class CtorLinksOverloadedCtors:

    @staticmethod
    def create(input: str) -> CtorLinksOverloadedCtors:
        ...

    @staticmethod
    def create(input: str, flag: bool) -> CtorLinksOverloadedCtors:
        """"""
        ...

