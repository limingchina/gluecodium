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

"""Lambda (callback) tests for the Python (pybind11) bindings."""

import functional
from test.lambdas import Lambdas, Concatenator

import pytest


class _Concatenator(Concatenator):
    def __init__(self, delimiter):
        super().__init__()
        self.delimiter = delimiter

    def invoke(self, first: str, second: str) -> str:
        return f"{first}{self.delimiter}{second}"


class TestLambdas:
    def test_concatenate(self):
        concatenator = _Concatenator("-")
        result = Lambdas.concatenate("a", "b", concatenator)

        assert result == "a-b"

    def test_get_concatenator(self):
        concatenator = Lambdas.get_concatenator("|")

        assert concatenator is not None
