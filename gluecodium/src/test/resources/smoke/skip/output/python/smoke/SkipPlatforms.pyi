

from enum import Enum
import typing

class SkipPlatforms:

    @staticmethod
    def not_in_java(input: str) -> str:
        ...

    @staticmethod
    def not_in_swift(input: bool) -> bool:
        ...

    @staticmethod
    def not_in_dart(input: float) -> float:
        ...

    @staticmethod
    def not_in_kotlin(input: float) -> float:
        ...


