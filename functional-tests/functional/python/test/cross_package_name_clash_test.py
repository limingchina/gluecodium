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

"""Cross-package name clash tests for the Python (pybind11) bindings.

Verifies that the same type name (``Alphabet``) defined in three different
packages (``test``, ``test.foo``, ``test.bar``) can be imported and used
simultaneously without import-path collisions.
"""

import functional
from test.Alphabet import Alphabet as RootAlphabet
from test.foo.Alphabet import Alphabet as FooAlphabet
from test.bar.Alphabet import Alphabet as BarAlphabet
from test.LearnToRead import LearnToRead
from test.LearnToReadAgain import LearnToReadAgain
from test.NameClashLists import NameClashLists

import pytest


class TestCrossPackageNameClash:
    # --- Three distinct Alphabet enums ---

    def test_root_alphabet_enum(self):
        """The top-level ``test.Alphabet`` enum is importable with correct values."""
        assert RootAlphabet.A is not None
        assert RootAlphabet.B is not None
        assert RootAlphabet.C is not None

    def test_foo_alphabet_enum(self):
        """The ``test.foo.Alphabet`` enum is importable with correct values."""
        assert FooAlphabet.ALPHA is not None
        assert FooAlphabet.BETA is not None
        assert FooAlphabet.GAMMA is not None

    def test_bar_alphabet_enum(self):
        """The ``test.bar.Alphabet`` enum is importable with correct values."""
        assert BarAlphabet.ALEPH is not None
        assert BarAlphabet.BEIT is not None
        assert BarAlphabet.GIMEL is not None

    def test_enums_are_distinct_types(self):
        """All three Alphabet enums are distinct types, not aliases."""
        assert RootAlphabet is not FooAlphabet
        assert RootAlphabet is not BarAlphabet
        assert FooAlphabet is not BarAlphabet

    # --- Structs referencing two clashing types ---

    def test_learn_to_read_default_values(self):
        """``LearnToRead`` default values use the correct Alphabet from each package."""
        instance = LearnToRead()
        assert instance.field_a == RootAlphabet.A
        assert instance.field_b == FooAlphabet.BETA

    def test_learn_to_read_set_fields(self):
        """``LearnToRead`` fields can be set with the correct enum types."""
        instance = LearnToRead(field_a=RootAlphabet.C, field_b=FooAlphabet.GAMMA)
        assert instance.field_a == RootAlphabet.C
        assert instance.field_b == FooAlphabet.GAMMA

    # --- Structs referencing foo + bar clash ---

    def test_learn_to_read_again_default_values(self):
        """``LearnToReadAgain`` default values use foo and bar Alphabet enums."""
        instance = LearnToReadAgain()
        assert instance.field_b == FooAlphabet.BETA
        assert instance.field_c == BarAlphabet.GIMEL

    def test_learn_to_read_again_set_fields(self):
        """``LearnToReadAgain`` fields can be set with the correct enum types."""
        instance = LearnToReadAgain(field_b=FooAlphabet.ALPHA, field_c=BarAlphabet.ALEPH)
        assert instance.field_b == FooAlphabet.ALPHA
        assert instance.field_c == BarAlphabet.ALEPH

    # --- Structs with lists of clashing types ---

    def test_name_clash_lists_default_empty(self):
        """``NameClashLists`` defaults to empty lists of the correct enum types."""
        instance = NameClashLists()
        assert instance.field_a == []
        assert instance.field_b == []

    def test_name_clash_lists_with_values(self):
        """``NameClashLists`` lists accept the correct Alphabet enum values."""
        instance = NameClashLists(
            field_a=[RootAlphabet.A, RootAlphabet.B],
            field_b=[FooAlphabet.ALPHA, FooAlphabet.BETA],
        )
        assert instance.field_a == [RootAlphabet.A, RootAlphabet.B]
        assert instance.field_b == [FooAlphabet.ALPHA, FooAlphabet.BETA]
