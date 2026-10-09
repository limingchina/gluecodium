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
from test.StaticBooleanMethods import StaticBooleanMethods
from test.StaticFloatDoubleMethods import StaticFloatDoubleMethods
from test.StaticIntMethods import StaticIntMethods

import pytest


class TestBooleanMethods:
    def test_return_inverted_boolean(self):
        assert StaticBooleanMethods.return_inverted_boolean(True) is False
        assert StaticBooleanMethods.return_inverted_boolean(False) is True

    def test_return_and_boolean(self):
        assert StaticBooleanMethods.return_and_boolean(True, True) is True
        assert StaticBooleanMethods.return_and_boolean(True, False) is False


class TestFloatDoubleMethods:
    def test_return_float(self):
        assert StaticFloatDoubleMethods.return_float(1.5) == pytest.approx(1.5)

    def test_return_incremented_float(self):
        assert StaticFloatDoubleMethods.return_incremented_float(1.5) == pytest.approx(2.5)

    def test_sum_two_floats(self):
        assert StaticFloatDoubleMethods.sum_two_floats(1.5, 2.5) == pytest.approx(4.0)

    def test_return_double(self):
        assert StaticFloatDoubleMethods.return_double(1.5) == pytest.approx(1.5)

    def test_return_incremented_double(self):
        assert StaticFloatDoubleMethods.return_incremented_double(1.5) == pytest.approx(2.5)

    def test_sum_two_doubles(self):
        assert StaticFloatDoubleMethods.sum_two_doubles(1.5, 2.5) == pytest.approx(4.0)


class TestIntMethods:
    def test_return_next_number_int8(self):
        assert StaticIntMethods.return_next_number_int8(1) == 2

    def test_sum_two_numbers_int8(self):
        assert StaticIntMethods.sum_two_numbers_int8(1, 2) == 3

    def test_return_prime_int8(self):
        assert StaticIntMethods.return_prime_int8() == 2

    def test_return_next_number_uint8(self):
        assert StaticIntMethods.return_next_number_uint8(1) == 2

    def test_return_prime_uint8(self):
        assert StaticIntMethods.return_prime_uint8() == 131

    def test_return_next_number_int16(self):
        assert StaticIntMethods.return_next_number_int16(1) == 2

    def test_return_prime_int16(self):
        assert StaticIntMethods.return_prime_int16() == 257

    def test_return_next_number_uint16(self):
        assert StaticIntMethods.return_next_number_uint16(1) == 2

    def test_return_prime_uint16(self):
        assert StaticIntMethods.return_prime_uint16() == 32771

    def test_return_next_number_int32(self):
        assert StaticIntMethods.return_next_number_int32(1) == 2

    def test_return_prime_int32(self):
        assert StaticIntMethods.return_prime_int32() == 65537

    def test_return_next_number_uint32(self):
        assert StaticIntMethods.return_next_number_uint32(1) == 2

    def test_return_prime_uint32(self):
        assert StaticIntMethods.return_prime_uint32() == 2147483659

    def test_return_next_number_int64(self):
        assert StaticIntMethods.return_next_number_int64(1) == 2

    def test_return_prime_int64(self):
        assert StaticIntMethods.return_prime_int64() == 4294967311

    def test_return_next_number_uint64(self):
        assert StaticIntMethods.return_next_number_uint64(1) == 2

    def test_return_prime_uint64(self):
        assert StaticIntMethods.return_prime_uint64() == 4294967311
