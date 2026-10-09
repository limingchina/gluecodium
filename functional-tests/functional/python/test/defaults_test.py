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

"""Default value mapping tests for the Python (pybind11) bindings."""

import functional
from test.Defaults import Defaults

DefaultsStructWithDefaults = Defaults.StructWithDefaults

import pytest


class TestDefaults:
    def test_default_struct_fields(self):
        value = Defaults.get_default()

        assert isinstance(value, DefaultsStructWithDefaults)
        assert value.int_field == 42
        assert value.uint_field == 4294967295
        assert value.float_field == pytest.approx(3.14)
        assert value.bool_field is True
        assert value.string_field == "some string"

    def test_struct_field_mutation(self):
        value = DefaultsStructWithDefaults()
        value.int_field = 7
        value.string_field = "changed"

        assert value.int_field == 7
        assert value.string_field == "changed"
