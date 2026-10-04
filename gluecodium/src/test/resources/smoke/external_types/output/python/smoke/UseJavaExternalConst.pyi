

from smoke.JavaExternalCtor import JavaExternalCtor
from enum import Enum
import typing
from typing import Optional

class UseJavaExternalConst:

    string_field: str


    _DEFAULT_TRUTH = JavaExternalCtor("foo")
