// -------------------------------------------------------------------------------------------------
// Copyright (C) 2020 HERE Europe B.V.
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

#include "unit/test/CommonMainFoo.h"

#include "gluecodium/TypeRepository.h"

#ifndef COMMON_INTERNAL
# error "COMMON_INTERNAL must be defined"
#endif

#ifndef COMMON_EXPORT
# error "COMMON_EXPORT must be defined"
#endif

#ifndef MODULE1_SHARED
# error "MODULE1_SHARED must be defined"
#endif

#ifndef MODULE1_INTERNAL
# error "MODULE1_INTERNAL must be defined"
#endif

namespace unit::test {
std::shared_ptr<CommonMainFoo>
CommonMainFoo::make()
{
    return nullptr;
}
} // namespace unit::test
