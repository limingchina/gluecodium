/*
 * Copyright (C) 2016-2026 HERE Europe B.V.
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

package com.here.gluecodium.generator.js

import com.here.gluecodium.generator.common.ImportsResolver
import com.here.gluecodium.generator.common.Include
import com.here.gluecodium.generator.cpp.CppIncludeResolver
import com.here.gluecodium.generator.cpp.CppNameRules
import com.here.gluecodium.model.lime.LimeElement
import com.here.gluecodium.model.lime.LimeException
import com.here.gluecodium.model.lime.LimeLambda
import com.here.gluecodium.model.lime.LimeTypeAlias
import com.here.gluecodium.model.lime.LimeTypeRef

/**
 * Resolves C++ includes needed by the generated embind binding code. Delegates to the existing
 * [CppIncludeResolver] (which already knows about the generated C++ headers, STL types, and the
 * Gluecodium helper includes such as `Return.h`).
 *
 * Enum-based exceptions are represented as `std::error_code` in C++ (no dedicated header is
 * generated), so exception declarations and references to enum-based exceptions are skipped.
 */
internal class EmbindIncludeResolver(
    limeReferenceMap: Map<String, LimeElement>,
    cppNameRules: CppNameRules,
    internalNamespace: List<String>,
) : ImportsResolver<Include> {
    private val cppIncludeResolver = CppIncludeResolver(limeReferenceMap, cppNameRules, internalNamespace)

    override fun resolveElementImports(limeElement: LimeElement): List<Include> =
        when {
            limeElement is LimeException -> emptyList()
            limeElement is LimeTypeRef && limeElement.type.actualType is LimeException -> emptyList()
            limeElement is LimeTypeRef && limeElement.type is LimeLambda ->
                cppIncludeResolver.resolveElementImports(limeElement) +
                    resolveLambdaTypeImports(limeElement.type as LimeLambda)
            limeElement is LimeTypeRef && limeElement.type is LimeTypeAlias ->
                cppIncludeResolver.resolveElementImports(limeElement) +
                    resolveElementImports((limeElement.type as LimeTypeAlias).typeRef)
            limeElement is LimeTypeAlias ->
                cppIncludeResolver.resolveElementImports(limeElement) + resolveElementImports(limeElement.typeRef)
            limeElement is LimeLambda ->
                cppIncludeResolver.resolveElementImports(limeElement) + resolveLambdaTypeImports(limeElement)
            else -> cppIncludeResolver.resolveElementImports(limeElement)
        }

    private fun resolveLambdaTypeImports(limeLambda: LimeLambda): List<Include> =
        (limeLambda.parameters.map { it.typeRef } + limeLambda.returnType.typeRef)
            .flatMap { resolveElementImports(it) }
}
