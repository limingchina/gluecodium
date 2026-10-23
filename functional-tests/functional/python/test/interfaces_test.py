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

"""Interface (callback) tests for the Python (pybind11) bindings."""

import functional
from test.InterfacesFactory import InterfacesFactory

import pytest


class TestInterfaces:
    def test_set_same_type_interfaces(self):
        input1 = InterfacesFactory.create_simple_interface_one()
        input1.set_string_value("one")
        input2 = InterfacesFactory.create_simple_interface_one()
        input2.set_string_value("two")
        nested = InterfacesFactory.create_nested_interface_one()

        nested.set_same_type_interfaces(input1, input2)
        result1 = nested.get_interface_one()
        result2 = nested.get_interface_two()

        assert result1.get_string_value() == "one"
        assert result2.get_string_value() == "two"

    def test_set_same_type_interfaces_identical(self):
        input1 = InterfacesFactory.create_simple_interface_one()
        input1.set_string_value("one")
        nested = InterfacesFactory.create_nested_interface_one()

        nested.set_same_type_interfaces(input1, input1)
        result1 = nested.get_interface_one()
        result2 = nested.get_interface_two()

        assert result1.get_string_value() == "one"
        assert result2.get_string_value() == "one"
