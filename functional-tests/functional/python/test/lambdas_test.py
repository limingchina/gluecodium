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
    def setup_method(self):
        Lambdas.reset_real_concatenator()

    def teardown_method(self):
        Lambdas.reset_real_concatenator()

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

    # --- G2: Nullable lambdas ---

    def test_get_concatenator_or_null_with_value(self):
        concatenator = Lambdas.get_concatenator_or_null(">.<")

        assert concatenator is not None
        assert concatenator("foo", "bar") == "foo>.<bar"

    def test_get_concatenator_or_null_with_null(self):
        result = Lambdas.get_concatenator_or_null(None)

        assert result is None

    def test_concatenate_or_not_with_callable(self):
        result = Lambdas.concatenate_or_not("foo", "bar", lambda first, second: f"{first}>.<{second}")

        assert result == "foo>.<bar"

    def test_concatenate_or_not_with_null(self):
        result = Lambdas.concatenate_or_not("foo", "bar", None)

        assert result is None

    def test_get_nullable_confuser_with_value(self):
        confuser = Lambdas.get_nullable_confuser()

        producer = confuser("foo")

        assert producer is not None
        assert producer() == "foo"

    def test_get_nullable_confuser_with_null(self):
        confuser = Lambdas.get_nullable_confuser()

        result = confuser(None)

        assert result is None

    def test_apply_nullable_confuser_with_value(self):
        def confuser(value):
            if value is not None:
                return lambda: value
            return None

        producer = Lambdas.apply_nullable_confuser(confuser, "foo")

        assert producer is not None
        assert producer() == "foo"

    def test_apply_nullable_confuser_with_null(self):
        def confuser(value):
            if value is not None:
                return lambda: value
            return None

        result = Lambdas.apply_nullable_confuser(confuser, None)

        assert result is None
