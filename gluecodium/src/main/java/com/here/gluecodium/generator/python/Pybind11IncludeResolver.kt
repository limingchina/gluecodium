/*
 * Copyright (C) 2016-2025 HERE Europe B.V.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 *
 * SPDX-License-Identifier: Apache-2.0
 * License-Filename: LICENSE
 */

package com.here.gluecodium.generator.python

import com.here.gluecodium.generator.common.ImportsResolver
import com.here.gluecodium.generator.common.Include
import com.here.gluecodium.generator.cpp.CppIncludeResolver
import com.here.gluecodium.generator.cpp.CppNameRules
import com.here.gluecodium.model.lime.LimeElement
import com.here.gluecodium.model.lime.LimeException
import com.here.gluecodium.model.lime.LimeTypeRef

/**
 * Resolves C++ includes needed by the generated pybind11 binding code. Delegates to the existing
 * [CppIncludeResolver] (which already knows about the generated C++ headers, STL types, and the
 * Gluecodium helper includes such as `Return.h`).
 *
 * Exceptions are represented as `std::error_code` in C++ (no dedicated header is generated), so a
 * type reference whose target is a [LimeException] is skipped — its include would otherwise point
 * at a non-existent header. The required `Return.h` is already pulled in via `_return_caster.h`.
 */
internal class Pybind11IncludeResolver(
    limeReferenceMap: Map<String, LimeElement>,
    cppNameRules: CppNameRules,
    internalNamespace: List<String>,
) : ImportsResolver<Include> {
    private val cppIncludeResolver = CppIncludeResolver(limeReferenceMap, cppNameRules, internalNamespace)

    override fun resolveElementImports(limeElement: LimeElement): List<Include> =
        if (limeElement is LimeTypeRef && limeElement.type.actualType is LimeException) {
            emptyList()
        } else {
            cppIncludeResolver.resolveElementImports(limeElement)
        }
}
