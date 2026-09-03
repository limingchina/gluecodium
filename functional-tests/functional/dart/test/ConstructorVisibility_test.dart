// -------------------------------------------------------------------------------------------------
// Copyright (C) 2016-2026 HERE Europe B.V.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.
//
// SPDX-License-Identifier: Apache-2.0
// License-Filename: LICENSE
//
// -------------------------------------------------------------------------------------------------

import "package:test/test.dart";
import "package:functional/test.dart";
import "../test_suite.dart";

final _testSuite = TestSuite("ConstructorVisibility");

void main() {
  // Struct without explicit constructors and an internal field must not
  // expose a public all-args constructor in Dart. An instance can only be
  // obtained from the C++ side and round-tripped.
  _testSuite.test("Uninitialized fields with internal field round trip", () {
    final input =
        ConstructorVisibility.makeUninitializedFields("secret", true);

    final result = ConstructorVisibility.uninitializedFieldsRoundTrip(input);

    expect(result.publicField, true);
  });

  // Struct without explicit constructors, an internal field and one
  // initialized public field must not expose a public initialized-fields
  // constructor in Dart either.
  _testSuite.test("Initialized field with internal field round trip", () {
    final input =
        ConstructorVisibility.makeInitializedField("secret", true, 7);

    final result = ConstructorVisibility.initializedFieldRoundTrip(input);

    expect(result.publicField, true);
    expect(result.initializedField, 7);
  });

  // Struct without explicit constructors, whose default field values rely
  // on overloaded named field constructors of another struct. The
  // generated default constructor must resolve each default value to the
  // field constructor overload matching its argument count.
  _testSuite.test("Defaults via overloaded field constructors round trip",
      () {
    final input =
        ConstructorVisibilityInitializedPublicFieldsViaOverloadedFieldCtors();

    expect(input.initializedField1.field1, "abc");
    expect(input.initializedField1.field2, "def");
    expect(input.initializedField1.initializedField1, 9);
    expect(input.initializedField1.initializedField2, 11);

    expect(input.initializedField2.initializedField1, 123);
    expect(input.initializedField2.initializedField2, 101);

    expect(input.initializedField3.initializedField1, 77);
    expect(input.initializedField3.initializedField2, 101);

    final result = ConstructorVisibility.overloadedFieldCtorsRoundTrip(input);

    expect(result.initializedField1.field1, "abc");
    expect(result.initializedField2.initializedField1, 123);
    expect(result.initializedField3.initializedField2, 101);
  });
}
