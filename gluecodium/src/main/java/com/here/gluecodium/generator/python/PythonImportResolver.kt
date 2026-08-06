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
import com.here.gluecodium.model.lime.LimeAttributeType.PYTHON
import com.here.gluecodium.model.lime.LimeConstant
import com.here.gluecodium.model.lime.LimeElement
import com.here.gluecodium.model.lime.LimeExternalDescriptor
import com.here.gluecodium.model.lime.LimeFunction
import com.here.gluecodium.model.lime.LimeGenericType
import com.here.gluecodium.model.lime.LimeList
import com.here.gluecodium.model.lime.LimeLambda
import com.here.gluecodium.model.lime.LimeMap
import com.here.gluecodium.model.lime.LimeNamedElement
import com.here.gluecodium.model.lime.LimeSet
import com.here.gluecodium.model.lime.LimeType
import com.here.gluecodium.model.lime.LimeTypeAlias
import com.here.gluecodium.model.lime.LimeTypeRef
import com.here.gluecodium.model.lime.LimeValue

/**
 * Resolves Python import statements (`import <module>` / `from <module> import <name>`) for a
 * given LIME element. For user-defined types this produces an import of the generated Python
 * module that declares the type; external types resolve to their configured import path.
 */
internal class PythonImportResolver(
    private val limeReferenceMap: Map<String, LimeElement>,
    private val nameResolver: PythonNameResolver,
) : ImportsResolver<PythonImport> {
    override fun resolveElementImports(limeElement: LimeElement): List<PythonImport> =
        when (limeElement) {
            is LimeTypeRef -> resolveTypeImports(limeElement.type)
            is LimeGenericType -> resolveGenericTypeImports(limeElement)
            is LimeValue -> resolveValueImports(limeElement)
            is LimeType -> resolveTypeImports(limeElement)
            // Constants are emitted as module-level variables, never imported.
            is LimeConstant -> emptyList()
            // Throwing functions are bound in the pybind11 layer; the Return<T, Error>
            // type caster raises the specific Python exception registered by
            // Pybind11Exception.mustache. The exception type must be imported so the
            // Python wrapper can reference it (e.g. in type hints or try/except).
            is LimeFunction ->
                listOf(createImport(limeElement)) +
                    (limeElement.exception?.let { resolveTypeImports(it) } ?: emptyList())
            is LimeNamedElement -> listOf(createImport(limeElement))
            else -> emptyList()
        }

    private fun resolveTypeImports(limeType: LimeType): List<PythonImport> {
        if (limeType is LimeTypeAlias) return resolveTypeImports(limeType.typeRef.type)
        if (limeType is LimeLambda) {
            return listOf(createImport(limeType)) +
                limeType.parameters.flatMap { resolveTypeImports(it.typeRef.type) } +
                resolveTypeImports(limeType.returnType.typeRef.type)
        }
        if (limeType is com.here.gluecodium.model.lime.LimeBasicType) {
            return when (limeType.typeId) {
                com.here.gluecodium.model.lime.LimeBasicType.TypeId.DATE,
                com.here.gluecodium.model.lime.LimeBasicType.TypeId.DURATION,
                -> listOf(PythonImport("datetime"))
                else -> emptyList()
            }
        }
        // Generic containers are builtins in Python, but their element types may be generated
        // user-defined types and must be imported recursively.
        if (limeType is LimeGenericType) return resolveGenericTypeImports(limeType)
        // Exceptions ARE generated as Python modules (PythonException.mustache emits a
        // Python Exception subclass), so they must be imported like any other user-defined type.
        val externalImport = resolveExternalImport(limeType)
        if (externalImport != null) return listOf(externalImport)
        return listOf(createImport(limeType))
    }

    private fun resolveGenericTypeImports(limeType: LimeGenericType): List<PythonImport> =
        when (limeType) {
            is LimeList -> resolveTypeImports(limeType.elementType.type)
            is LimeSet -> resolveTypeImports(limeType.elementType.type)
            is LimeMap ->
                resolveTypeImports(limeType.keyType.type) + resolveTypeImports(limeType.valueType.type)
            else -> emptyList()
        }

    private fun resolveValueImports(limeValue: LimeValue): List<PythonImport> =
        when (limeValue) {
            is LimeValue.KeyValuePair ->
                resolveValueImports(limeValue.key) + resolveValueImports(limeValue.value)
            is LimeValue.InitializerList -> limeValue.values.flatMap { resolveValueImports(it) }
            is LimeValue.StructInitializer ->
                resolveTypeImports(limeValue.typeRef.type) + limeValue.values.flatMap { resolveValueImports(it) }
            // A constant reference is resolved in-place at the use site (e.g. `ENUM_CONSTANT =
            // StateEnum.ON`), not via a cross-module import. Emitting an import here would produce
            // a bogus `from test.<NAME> import <NAME>` for a submodule that is never generated.
            is LimeValue.Constant -> resolveTypeImports(limeValue.typeRef.type)
            else -> emptyList()
        }

    private fun resolveExternalImport(limeType: LimeType): PythonImport? {
        val importPath = limeType.external?.getFor(PYTHON)?.get(LimeExternalDescriptor.IMPORT_PATH_NAME)
        return if (importPath.isNullOrBlank()) {
            null
        } else {
            PythonImport(importPath, nameResolver.resolveName(limeType))
        }
    }

    private fun createImport(limeElement: LimeNamedElement): PythonImport {
        val topLevel = findTopLevelElement(limeElement)
        val modulePath =
            (topLevel.path.head + nameResolver.resolveName(topLevel))
                .joinToString(".")
        return PythonImport(modulePath, nameResolver.resolveName(topLevel))
    }

    /**
     * Finds the top-level (non-nested) ancestor of the given element by walking up the
     * parent chain via the reference map. Returns the element itself if it has no parent.
     */
    private fun findTopLevelElement(element: LimeNamedElement): LimeNamedElement {
        var current = element
        while (current.path.hasParent) {
            val parent =
                limeReferenceMap[current.path.parent.toString()] as? LimeNamedElement
                    ?: return current
            current = parent
        }
        return current
    }
}
