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

"""String type mapping tests for the Python (pybind11) bindings."""

import functional
from test.StaticStringMethods import StaticStringMethods
from test.StringsWithCstring import StringsWithCstring
from test.CppRefReturnType import CppRefReturnType

import pytest


class TestStaticStringMethods:
    def test_return_input_string(self):
        assert StaticStringMethods.return_input_string("abc") == "abc"

    def test_concatenate_strings(self):
        assert StaticStringMethods.concatenate_strings("a", "b") == "ab"

    def test_return_hello_string(self):
        assert StaticStringMethods.return_hello_string() == "hello"

    def test_return_empty(self):
        assert StaticStringMethods.return_empty() == ""


class TestStringsWithCstring:
    def test_return_input_string_type(self):
        assert StringsWithCstring.return_input_string_type("x") == "x"

    def test_return_input_string(self):
        assert StringsWithCstring.return_input_string("y") == "y"


class TestCppRefReturnType:
    def test_string_ref(self):
        assert CppRefReturnType.string_ref() == "nonsense"

    def test_string_property(self):
        assert CppRefReturnType.string_property() == "nonsense"
