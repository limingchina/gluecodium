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

import com.here.gluecodium.generator.common.NameResolver
import com.here.gluecodium.generator.cpp.CppNameCache
import com.here.gluecodium.generator.cpp.CppNameResolver
import com.here.gluecodium.generator.cpp.CppNameRules
import com.here.gluecodium.model.lime.LimeElement
import com.here.gluecodium.model.lime.LimeLambda
import com.here.gluecodium.model.lime.LimeNamedElement
import com.here.gluecodium.model.lime.LimeReturnType
import com.here.gluecodium.model.lime.LimeTypeRef

/**
 * Name resolver that exposes the C++ names used inside the generated embind binding code.
 *
 * <p>embind binding files `#include` the generated C++ headers and call the C++ API directly,
 * so the C++ names (qualified, following the C++ namespace) are what the binding code needs.
 * This resolver wraps a [CppNameResolver] configured with `forceFollowThrough` so that type
 * aliases are resolved to their underlying C++ type.
 */
internal class EmbindNameResolver(
    limeReferenceMap: Map<String, LimeElement>,
    internalNamespace: List<String>,
    private val nameCache: CppNameCache,
) : NameResolver {
    private val cppNameResolver =
        CppNameResolver(limeReferenceMap, internalNamespace, nameCache, forceFollowThrough = true)

    override fun resolveName(element: Any): String =
        when (element) {
            is LimeTypeRef -> resolveTypeRef(element)
            is LimeReturnType -> resolveTypeRef(element.typeRef)
            else -> cppNameResolver.resolveName(element)
        }

    override fun resolveGetterName(element: Any) = cppNameResolver.resolveGetterName(element)

    override fun resolveSetterName(element: Any) = cppNameResolver.resolveSetterName(element)

    /**
     * Resolve the fully-qualified C++ name (with namespace) for a named element, e.g.
     * `com::example::lifecycle::Producer`.
     */
    fun resolveFullName(element: LimeNamedElement): String = nameCache.getFullyQualifiedName(element)

    /**
     * Lambdas are emitted as C++ aliases; embind must see their underlying `std::function`
     * signature. Keep every non-lambda spelling delegated to [CppNameResolver].
     */
    private fun resolveTypeRef(limeTypeRef: LimeTypeRef): String {
        val limeLambda = limeTypeRef.type.actualType as? LimeLambda ?: return cppNameResolver.resolveName(limeTypeRef)
        val function = limeLambda.asFunction()
        val parameters =
            function.parameters.joinToString(", ") { parameter ->
                "const ${resolveName(parameter.typeRef)}" +
                    if (CppNameResolver.needsRefSuffix(parameter.typeRef)) "&" else ""
            }
        val functionType = "::std::function<${resolveName(function.returnType)}($parameters)>"
        return if (limeTypeRef.isNullable) "std::optional< $functionType >" else functionType
    }
}
