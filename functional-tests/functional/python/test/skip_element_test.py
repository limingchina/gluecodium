# Copyright (C) 2016-2025 HERE Europe B.V.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# SPDX-License-Identifier: Apache-2.0
# License-Filename: LICENSE

"""Skip-attribute mapping tests for the Python (pybind11) bindings.

The @Skip attribute is only applied for @Java, @Swift, @Dart and @Kotlin in the
functional LimeIDL fixtures, so all four methods should be present in the Python
bindings (Python is never skipped there).
"""

import functional
from test.SkipFunctions import SkipFunctions

import pytest


class TestSkipElement:
    def test_not_in_java_present(self):
        assert SkipFunctions.not_in_java("input") == "input"

    def test_not_in_swift_present(self):
        assert SkipFunctions.not_in_swift(True) is True

    def test_not_in_dart_present(self):
        assert SkipFunctions.not_in_dart(1.5) == 1.5

    def test_not_in_kotlin_present(self):
        assert SkipFunctions.not_in_kotlin("input") == "input"
