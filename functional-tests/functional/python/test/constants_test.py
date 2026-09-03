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

"""Constant mapping tests for the Python (pybind11) bindings."""

import functional
from test.Constants import Constants
from test.ConstantsSkipCpp import ConstantsSkipCpp

import pytest


class TestConstants:
    def test_int_constant(self):
        assert Constants.INT_CONSTANT == -11

    def test_uint_constant(self):
        assert Constants.UINT_CONSTANT == 4294967295

    def test_float_constant(self):
        assert Constants.FLOAT_CONSTANT == pytest.approx(2.71)

    def test_double_constant(self):
        assert Constants.DOUBLE_CONSTANT == pytest.approx(-3.14)

    def test_string_constant(self):
        assert Constants.STRING_CONSTANT == "Foo bar"

    def test_bool_constant(self):
        assert ConstantsSkipCpp.BOOL_CONSTANT is True
