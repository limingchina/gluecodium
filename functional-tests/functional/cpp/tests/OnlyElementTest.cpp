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

#include "test/OnlyFunctions.h"

#include <gmock/gmock.h>
#include <type_traits>

namespace test
{
namespace
{
// Fail compilation if a platform-only constant leaks into the C++ API.
template <typename T>
struct HasJavaConstant {
    template <typename U>
    static auto check(int) -> decltype(U::JAVA_CONSTANT, std::true_type{});
    template <typename>
    static auto check(...) -> std::false_type;
    static constexpr bool value = decltype(check<T>(0))::value;
};
static_assert(!HasJavaConstant<OnlyFunctions>::value, "Java constant must be excluded from C++");
template <typename T>
struct HasKotlinConstant {
    template <typename U>
    static auto check(int) -> decltype(U::KOTLIN_CONSTANT, std::true_type{});
    template <typename>
    static auto check(...) -> std::false_type;
    static constexpr bool value = decltype(check<T>(0))::value;
};
static_assert(!HasKotlinConstant<OnlyFunctions>::value, "Kotlin constant must be excluded from C++");
template <typename T>
struct HasSwiftConstant {
    template <typename U>
    static auto check(int) -> decltype(U::SWIFT_CONSTANT, std::true_type{});
    template <typename>
    static auto check(...) -> std::false_type;
    static constexpr bool value = decltype(check<T>(0))::value;
};
static_assert(!HasSwiftConstant<OnlyFunctions>::value, "Swift constant must be excluded from C++");
template <typename T>
struct HasDartConstant {
    template <typename U>
    static auto check(int) -> decltype(U::DART_CONSTANT, std::true_type{});
    template <typename>
    static auto check(...) -> std::false_type;
    static constexpr bool value = decltype(check<T>(0))::value;
};
static_assert(!HasDartConstant<OnlyFunctions>::value, "Dart constant must be excluded from C++");
}

TEST(OnlyElementTest, SelectedMethodsRoundTrip)
{
    const std::string input = "Only: native round trip";
    EXPECT_EQ(input, OnlyFunctions::java_only(input));
    EXPECT_EQ(input, OnlyFunctions::kotlin_only(input));
    EXPECT_EQ(input, OnlyFunctions::swift_only(input));
    EXPECT_EQ(input, OnlyFunctions::dart_only(input));
    EXPECT_EQ(input, OnlyFunctions::cpp_only(input));
    EXPECT_EQ(input, OnlyFunctions::shared(input));
}

TEST(OnlyElementTest, CppOnlyConstant)
{
    EXPECT_EQ(55, OnlyFunctions::CPP_CONSTANT);
}
}
