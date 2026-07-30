

import typing

class SkipProxy:

    def not_in_java(self, input: str) -> str:
        ...

    def not_in_swift(self, input: bool) -> bool:
        ...

    def not_in_dart(self, input: float) -> float:
        ...

    def not_in_kotlin(self, input: float) -> float:
        ...

    @property
    def skipped_in_java(self) -> str:
        ...

    @skipped_in_java.setter
    def skipped_in_java(self, value: str) -> None:
        ...

    @property
    def is_skipped_in_swift(self) -> bool:
        ...

    @is_skipped_in_swift.setter
    def is_skipped_in_swift(self, value: bool) -> None:
        ...

    @property
    def skipped_in_dart(self) -> float:
        ...

    @skipped_in_dart.setter
    def skipped_in_dart(self, value: float) -> None:
        ...

    @property
    def skipped_in_kotlin(self) -> float:
        ...

    @skipped_in_kotlin.setter
    def skipped_in_kotlin(self, value: float) -> None:
        ...

