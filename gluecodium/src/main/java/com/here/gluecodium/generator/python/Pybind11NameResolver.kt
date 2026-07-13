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

import com.here.gluecodium.generator.common.NameResolver
import com.here.gluecodium.generator.cpp.CppNameCache
import com.here.gluecodium.generator.cpp.CppNameResolver
import com.here.gluecodium.generator.cpp.CppNameRules
import com.here.gluecodium.model.lime.LimeElement
import com.here.gluecodium.model.lime.LimeNamedElement

/**
 * Name resolver that exposes the C++ names used inside the generated pybind11 binding code.
 *
 * <p>pybind11 binding files `#include` the generated C++ headers and call the C++ API directly,
 * so the C++ names (qualified, following the C++ namespace) are what the binding code needs. This
 * resolver wraps a [CppNameResolver] configured with `forceFollowThrough` so that type aliases are
 * resolved to their underlying C++ type.
 */
internal class Pybind11NameResolver(
    limeReferenceMap: Map<String, LimeElement>,
    internalNamespace: List<String>,
    nameCache: CppNameCache,
    cppNameRules: CppNameRules,
) : NameResolver {
    private val internalNs: List<String> = internalNamespace
    private val cppNameResolver =
        CppNameResolver(limeReferenceMap, internalNamespace, nameCache, forceFollowThrough = true)

    override fun resolveName(element: Any): String = cppNameResolver.resolveName(element)

    override fun resolveGetterName(element: Any) = cppNameResolver.resolveGetterName(element)

    override fun resolveSetterName(element: Any) = cppNameResolver.resolveSetterName(element)

    /**
     * Resolve the fully-qualified C++ name (with namespace) for a named element, e.g.
     * `com::example::lifecycle::Producer`. Built directly from the Lime path so it works for every
     * element (including exceptions, which have no dedicated C++ header) without relying on the
     * C++ name cache's per-element name rules.
     */
    fun resolveFullName(element: LimeNamedElement): String {
        val parts: List<String> = listOf("") + internalNs + element.path.head + element.path.tail
        return parts.joinToString("::")
    }
}
