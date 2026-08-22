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

import com.here.gluecodium.generator.common.ImportsResolver
import com.here.gluecodium.model.lime.LimeElement
import com.here.gluecodium.model.lime.LimeBasicType
import com.here.gluecodium.model.lime.LimeGenericType
import com.here.gluecodium.model.lime.LimeList
import com.here.gluecodium.model.lime.LimeMap
import com.here.gluecodium.model.lime.LimeNamedElement
import com.here.gluecodium.model.lime.LimeSet
import com.here.gluecodium.model.lime.LimeType
import com.here.gluecodium.model.lime.LimeTypeAlias
import com.here.gluecodium.model.lime.LimeTypeRef

/**
 * Resolves TypeScript import statements for a given LIME element. For user-defined types this
 * produces a relative import of the generated `.d.ts` module that declares the type.
 */
internal class JsImportResolver(
    private val limeReferenceMap: Map<String, LimeElement>,
    private val nameRules: JsNameRules,
) : ImportsResolver<JsImport> {
    override fun resolveElementImports(limeElement: LimeElement): List<JsImport> =
        when (limeElement) {
            is LimeTypeRef -> resolveTypeImports(limeElement.type.actualType)
            is LimeGenericType -> resolveGenericTypeImports(limeElement)
            is LimeType -> resolveTypeImports(limeElement.actualType)
            is LimeNamedElement -> listOf(createImport(limeElement))
            else -> emptyList()
        }

    private fun resolveTypeImports(limeType: LimeType): List<JsImport> =
        when (limeType) {
            is LimeBasicType -> emptyList()
            is LimeTypeAlias -> resolveTypeImports(limeType.typeRef.type.actualType)
            is LimeGenericType -> resolveGenericTypeImports(limeType)
            is LimeNamedElement -> listOf(createImport(limeType))
            else -> emptyList()
        }

    private fun resolveGenericTypeImports(limeType: LimeGenericType): List<JsImport> =
        when (limeType) {
            is LimeList -> resolveTypeImports(limeType.elementType.type.actualType)
            is LimeSet -> resolveTypeImports(limeType.elementType.type.actualType)
            is LimeMap ->
                resolveTypeImports(limeType.keyType.type.actualType) +
                    resolveTypeImports(limeType.valueType.type.actualType)
            else -> emptyList()
        }

    private fun createImport(limeElement: LimeNamedElement): JsImport {
        val topLevel = findTopLevelElement(limeElement)
        val modulePath = "./" + (topLevel.path.head + nameRules.getName(topLevel)).joinToString("/")
        return JsImport(modulePath, nameRules.getName(topLevel))
    }

    private fun findTopLevelElement(element: LimeNamedElement): LimeNamedElement {
        var current = element
        while (current.path.hasParent) {
            val parent = limeReferenceMap[current.path.parent.toString()] as? LimeNamedElement ?: return current
            current = parent
        }
        return current
    }
}
