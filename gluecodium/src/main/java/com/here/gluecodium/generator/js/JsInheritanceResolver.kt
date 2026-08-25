/*
 * Copyright (C) 2026 HERE Europe B.V.
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

import com.here.gluecodium.generator.cpp.CppNameCache
import com.here.gluecodium.model.lime.LimeContainerWithInheritance
import com.here.gluecodium.model.lime.LimeFunction
import com.here.gluecodium.model.lime.LimeModel
import com.here.gluecodium.model.lime.LimeProperty
import com.here.gluecodium.model.lime.LimeType

internal class JsInheritanceResolver(
    private val nameRules: JsNameRules,
    private val cppNameCache: CppNameCache,
) {
    /** Prefers an `open class` parent over a narrow interface as the single embind `base<>`. */
    fun primaryBaseType(
        type: LimeType,
        filteredModel: LimeModel,
    ): LimeContainerWithInheritance? =
        (type as? LimeContainerWithInheritance)?.parents
            ?.mapNotNull { it.type.actualType as? LimeContainerWithInheritance }
            ?.filter { filteredModel.referenceMap.containsKey(it.fullName) }
            ?.minByOrNull { it is com.here.gluecodium.model.lime.LimeInterface }

    fun secondaryParentMembers(
        type: LimeType,
        filteredModel: LimeModel,
    ): Pair<List<LimeFunction>, List<LimeProperty>> {
        val container = type as? LimeContainerWithInheritance ?: return emptyList<LimeFunction>() to emptyList()
        val primaryBase = primaryBaseType(type, filteredModel)
        val secondaryParents =
            container.parents
                .mapNotNull { it.type.actualType as? LimeContainerWithInheritance }
                .filter { it !== primaryBase && filteredModel.referenceMap.containsKey(it.fullName) }
        val functions =
            secondaryParents
                .flatMap { it.functions + it.inheritedFunctions }
                .distinctBy { it.fullName }
        val properties =
            secondaryParents
                .flatMap { it.properties + it.inheritedProperties }
                .distinctBy { it.fullName }
        return functions to properties
    }

    fun primaryInheritedOverloads(
        type: LimeType,
        filteredModel: LimeModel,
    ): List<LimeFunction> {
        val container = type as? LimeContainerWithInheritance ?: return emptyList()
        val primaryBase = primaryBaseType(type, filteredModel) ?: return emptyList()
        val ownNames = container.functions
            .filterNot { it.isStatic || it.isConstructor }
            .map { nameRules.getName(it) }
            .toSet()
        if (ownNames.isEmpty()) return emptyList()
        return (primaryBase.functions + primaryBase.inheritedFunctions)
            .filter { !it.isStatic && nameRules.getName(it) in ownNames }
            .distinctBy { it.fullName }
    }
}