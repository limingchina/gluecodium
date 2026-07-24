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

from test.Lambdas import Lambdas


class TestLambdas:
    def test_concatenate(self):
        result = Lambdas.concatenate("a", "b", lambda first, second: f"{first}-{second}")

        assert result == "a-b"

    def test_get_concatenator(self):
        concatenator = Lambdas.get_concatenator("|")

        assert concatenator("a", "b") == "a|b"

    def test_compose_concatenators(self):
        concatenator = Lambdas.compose_concatenators(
            lambda first, second: f"{first}-{second}",
            lambda first, second: f"{first}|{second}",
        )

        assert concatenator("a", "b", "c") == "a-b|c"

    def test_concatenate_list(self):
        result = Lambdas.concatenate_list(
            ["a", "b", "c"],
            [lambda first, second: f"{first}-{second}", lambda first, second: f"{first}|{second}"],
        )

        assert result == "a-b|c"

    def test_static_lambda_property(self):
        Lambdas.real_concatenator_set(lambda first, second: f"{first}:{second}")

        assert Lambdas.real_concatenator()("a", "b") == "a:b"
