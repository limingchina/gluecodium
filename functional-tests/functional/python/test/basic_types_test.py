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

"""Basic type mapping tests for the Python (pybind11) bindings."""

import functional
from test.basic_types import BasicTypes

import pytest


class TestBasicTypes:
    def test_string_function(self):
        assert BasicTypes.string_function("hello") == "hello"

    def test_bool_function(self):
        assert BasicTypes.bool_function(True) is True

    def test_int_function(self):
        assert BasicTypes.int_function(42) == 42

    def test_float_function(self):
        assert BasicTypes.float_function(3.14) == pytest.approx(3.14)

    def test_byte_function(self):
        assert BasicTypes.byte_function(7) == 7
