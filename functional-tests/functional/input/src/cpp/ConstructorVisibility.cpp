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

#include "test/ConstructorVisibility.h"

namespace test
{

ConstructorVisibility::NoCtorsUninitializedFieldsOneInternalField
ConstructorVisibility::make_uninitialized_fields(
    const std::string& internal_field,
    const bool public_field )
{
    return { internal_field, public_field };
}

ConstructorVisibility::NoCtorsUninitializedFieldsOneInternalField
ConstructorVisibility::uninitialized_fields_round_trip(
    const ConstructorVisibility::NoCtorsUninitializedFieldsOneInternalField& input )
{
    return input;
}

ConstructorVisibility::NoCtorsInitializedPublicFieldOneInternalField
ConstructorVisibility::make_initialized_field(
    const std::string& internal_field,
    const bool public_field,
    const int32_t initialized_field )
{
    return { internal_field, public_field, initialized_field };
}

ConstructorVisibility::NoCtorsInitializedPublicFieldOneInternalField
ConstructorVisibility::initialized_field_round_trip(
    const ConstructorVisibility::NoCtorsInitializedPublicFieldOneInternalField& input )
{
    return input;
}

ConstructorVisibility::InitializedPublicFieldsViaOverloadedFieldCtors
ConstructorVisibility::overloaded_field_ctors_round_trip(
    const ConstructorVisibility::InitializedPublicFieldsViaOverloadedFieldCtors& input )
{
    return input;
}

}  // namespace test
