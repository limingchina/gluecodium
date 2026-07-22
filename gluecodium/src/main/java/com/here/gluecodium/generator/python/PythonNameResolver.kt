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

import com.here.gluecodium.cli.GluecodiumExecutionException
import com.here.gluecodium.common.LimeLogger
import com.here.gluecodium.generator.common.CommentsProcessor
import com.here.gluecodium.generator.common.NameResolver
import com.here.gluecodium.generator.common.ReferenceMapBasedResolver
import com.here.gluecodium.model.lime.LimeAttributeType.PYTHON
import com.here.gluecodium.model.lime.LimeAttributeValueType.NAME
import com.here.gluecodium.model.lime.LimeBasicType
import com.here.gluecodium.model.lime.LimeComment
import com.here.gluecodium.model.lime.LimeElement
import com.here.gluecodium.model.lime.LimeList
import com.here.gluecodium.model.lime.LimeMap
import com.here.gluecodium.model.lime.LimeNamedElement
import com.here.gluecodium.model.lime.LimeReturnType
import com.here.gluecodium.model.lime.LimeSet
import com.here.gluecodium.model.lime.LimeType
import com.here.gluecodium.model.lime.LimeTypeAlias
import com.here.gluecodium.model.lime.LimeTypeRef
import com.here.gluecodium.model.lime.LimeValue

/**
 * Main name resolver for the Python generator. Resolves Python-side names for types, type
 * references and comments. Type names are resolved as own (unqualified) names.
 */
internal class PythonNameResolver(
    limeReferenceMap: Map<String, LimeElement>,
    private val nameRules: PythonNameRules,
    private val limeLogger: LimeLogger,
    private val commentsProcessor: CommentsProcessor,
) : ReferenceMapBasedResolver(limeReferenceMap), NameResolver {
    override fun resolveName(element: Any): String = resolvePythonType(element)

    private fun resolvePythonType(element: Any, requiresHashable: Boolean = false): String =
        when (element) {
            is LimeComment -> resolveComment(element)
            is LimeBasicType -> resolveBasicType(element)
            is LimeReturnType -> resolvePythonType(element.typeRef, requiresHashable)
            is LimeTypeRef -> {
                val typeName = resolvePythonType(element.type, requiresHashable)
                if (element.isNullable) "Optional[" + typeName + "]" else typeName
            }
            is LimeList -> {
                val elementType = resolvePythonType(element.elementType, requiresHashable)
                if (requiresHashable) "tuple[" + elementType + ", ...]" else "list[" + elementType + "]"
            }
            is LimeSet -> {
                val elementType = resolvePythonType(element.elementType, true)
                if (requiresHashable) "frozenset[" + elementType + "]" else "set[" + elementType + "]"
            }
            is LimeMap -> {
                val keyType = resolvePythonType(element.keyType, true)
                val valueType = resolvePythonType(element.valueType, requiresHashable)
                if (requiresHashable) {
                    "frozenset[tuple[" + keyType + ", " + valueType + "]]"
                } else {
                    "dict[" + keyType + ", " + valueType + "]"
                }
            }
            is LimeTypeAlias -> resolvePythonType(element.typeRef, requiresHashable)
            is LimeType -> nameRules.getName(element)
            is LimeNamedElement -> getPlatformName(element) ?: nameRules.getName(element)
            is LimeValue -> resolveValue(element)
            else -> throw GluecodiumExecutionException("Unsupported element type ${element.javaClass.name}")
        }


    private fun resolveComment(limeComment: LimeComment): String {
        val commentText = limeComment.getFor("Python")
        if (commentText.isBlank()) return ""
        val commentedElement = limeReferenceMap[limeComment.path.toString()] as? LimeNamedElement
            ?: getParentElement(limeComment.path)
        return commentsProcessor.process(commentedElement.fullName, commentText, emptyMap(), limeLogger)
    }

    private fun resolveBasicType(limeBasicType: LimeBasicType): String {
        // Placeholder mapping; the full Python type mapping is implemented in Phase 4.
        return when (limeBasicType.typeId) {
            LimeBasicType.TypeId.VOID -> "None"
            LimeBasicType.TypeId.BOOLEAN -> "bool"
            LimeBasicType.TypeId.STRING -> "str"
            LimeBasicType.TypeId.BLOB -> "bytes"
            LimeBasicType.TypeId.FLOAT, LimeBasicType.TypeId.DOUBLE -> "float"
            LimeBasicType.TypeId.DATE -> "datetime.datetime"
            LimeBasicType.TypeId.DURATION -> "datetime.timedelta"
            LimeBasicType.TypeId.LOCALE -> "str"
            else -> "int"
        }
    }

    /**
     * Resolves the dotted module path (e.g. `test.InstanceInStruct`) that declares the given type
     * reference. Used to emit a local, deferred `from <module> import <name>` statement (as
     * opposed to a module-level one) for types that would otherwise form a circular import, such
     * as a nested struct field referencing its own enclosing type.
     */
    override fun resolveReferenceName(element: Any): String? {
        val limeType = when (element) {
            is LimeTypeRef -> element.type.actualType
            is LimeType -> element.actualType
            else -> return null
        }
        val namedType = limeType as? LimeNamedElement ?: return null
        return (namedType.path.head + resolveName(namedType)).joinToString(".")
    }

    private fun resolveValue(limeValue: LimeValue): String {
        // Special float literals (NaN / Infinity) are not Python builtins; render as float() calls.
        if (limeValue is LimeValue.Special) {
            return when (limeValue.value) {
                LimeValue.Special.ValueId.NAN -> "float('nan')"
                LimeValue.Special.ValueId.INFINITY -> "float('inf')"
                LimeValue.Special.ValueId.NEGATIVE_INFINITY -> "float('-inf')"
            }
        }
        if (limeValue !is LimeValue.Literal) return limeValue.toString()
        val actualType = limeValue.typeRef.type.actualType
        // Boolean literals must use Python's capitalized True/False (LimeValue.Literal.toString()
        // returns the lowercase "true"/"false" used by most LIME targets).
        if (actualType is LimeBasicType && actualType.typeId == LimeBasicType.TypeId.BOOLEAN) {
            return when (limeValue.value) {
                "true" -> "True"
                "false" -> "False"
                else -> limeValue.value
            }
        }
        return limeValue.toString()
    }

    private fun getPlatformName(limeElement: LimeNamedElement): String? = limeElement.attributes.get(PYTHON, NAME)
}
