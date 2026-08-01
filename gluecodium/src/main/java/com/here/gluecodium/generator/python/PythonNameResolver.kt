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
import com.here.gluecodium.model.lime.LimeLambda
import com.here.gluecodium.model.lime.LimeList
import com.here.gluecodium.model.lime.LimeMap
import com.here.gluecodium.model.lime.LimeNamedElement
import com.here.gluecodium.model.lime.LimePath
import com.here.gluecodium.model.lime.LimeReturnType
import com.here.gluecodium.model.lime.LimeSet
import com.here.gluecodium.model.lime.LimeType
import com.here.gluecodium.model.lime.LimeTypeAlias
import com.here.gluecodium.model.lime.LimeTypeRef
import com.here.gluecodium.model.lime.LimeValue

/**
 * Main name resolver for the Python generator. Resolves Python-side names for types, type
 * references and comments. Type names are resolved as own (unqualified) names.
 *
 * Module paths are derived from the element's own name so that each type gets its own Python
 * module (e.g. `test.InstanceInStruct` for the `InstanceInStruct` type in package `test`).
 */
internal class PythonNameResolver(
    limeReferenceMap: Map<String, LimeElement>,
    private val nameRules: PythonNameRules,
    private val limeLogger: LimeLogger,
    private val commentsProcessor: CommentsProcessor,
) : ReferenceMapBasedResolver(limeReferenceMap), NameResolver {
    override fun resolveName(element: Any): String = resolvePythonType(element)

    private fun resolvePythonType(
        element: Any,
        requiresHashable: Boolean = false,
    ): String =
        when (element) {
            is LimeComment -> resolveComment(element)
            is LimeBasicType -> resolveBasicType(element)
            is LimeReturnType -> resolvePythonType(element.typeRef, requiresHashable)
            is LimeTypeRef -> {
                val actualType = element.type.actualType
                val typeName =
                    (actualType as? LimeLambda)
                        ?.let(::resolveLambdaType)
                        ?: if (actualType.path.hasParent)
                            resolveQualifiedTypeName(actualType)
                        else
                            resolvePythonType(actualType, requiresHashable)
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
        val commentedElement =
            limeReferenceMap[limeComment.path.toString()] as? LimeNamedElement
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

    private fun resolveLambdaType(limeLambda: LimeLambda): String {
        val function = limeLambda.asFunction()
        val parameters = function.parameters.joinToString(", ") { resolvePythonType(it.typeRef) }
        return "Callable[[$parameters], ${resolvePythonType(function.returnType)}]"
    }

    /**
     * Resolves the dotted module path (e.g. `test.InstanceInStruct`) that declares the given type
     * reference. Used to emit a local, deferred `from <module> import <name>` statement (as
     * opposed to a module-level one) for types that would otherwise form a circular import, such
     * as a nested struct field referencing its own enclosing type.
     */
    override fun resolveReferenceName(element: Any): String? {
        val limeType =
            when (element) {
                is LimeTypeRef -> element.type.actualType
                is LimeType -> element.actualType
                else -> return null
            }
        val namedType = limeType as? LimeNamedElement ?: return null
        val topLevel = findTopLevelElement(namedType)
        return (topLevel.path.head + nameRules.getName(topLevel)).joinToString(".")
    }

    /**
     * Resolves the fully-qualified Python name for a type, including parent qualifiers for
     * nested types (e.g. `Outer.Inner` for a type nested inside `Outer`). Top-level types
     * resolve to their short name. This is used for type references (annotations, _wrap()
     * arguments) where the full attribute path is needed to access the type at runtime.
     */
    private fun resolveQualifiedTypeName(limeType: LimeType): String {
        if (!limeType.path.hasParent) return nameRules.getName(limeType)
        // Walk the path tail, looking up each ancestor in the reference map and resolving
        // its (short) name. This produces a dotted qualified name like `Outer.Inner`.
        val head = limeType.path.head
        val tail = limeType.path.tail
        val sb = StringBuilder()
        var currentFullPath: String? = null
        for (component in tail) {
            currentFullPath =
                if (currentFullPath == null)
                    if (head.isNotEmpty()) head.joinToString(".") + "." + component else component
                else
                    "$currentFullPath.$component"
            val element = limeReferenceMap[currentFullPath] as? LimeNamedElement
            val name = if (element != null) nameRules.getName(element) else component
            if (sb.isNotEmpty()) sb.append(".")
            sb.append(name)
        }
        return sb.toString()
    }

    /**
     * Finds the top-level (non-nested) ancestor of the given element by walking up the
     * parent chain via the reference map. Returns the element itself if it has no parent.
     */
    private fun findTopLevelElement(element: LimeNamedElement): LimeNamedElement {
        var current = element
        while (current.path.hasParent) {
            val parent = limeReferenceMap[current.path.parent.toString()] as? LimeNamedElement
                ?: return current
            current = parent
        }
        return current
    }

    private fun resolveValue(limeValue: LimeValue): String =
        when (limeValue) {
            is LimeValue.Special -> {
                when (limeValue.value) {
                    LimeValue.Special.ValueId.NAN -> "float('nan')"
                    LimeValue.Special.ValueId.INFINITY -> "float('inf')"
                    LimeValue.Special.ValueId.NEGATIVE_INFINITY -> "float('-inf')"
                }
            }
            is LimeValue.Constant -> {
                val limeElement = limeValue.valueRef.element
                val parentElement = getParentElement(limeElement)
                "${resolveName(parentElement)}.${resolveName(limeElement)}"
            }
            is LimeValue.Literal -> {
                val actualType = limeValue.typeRef.type.actualType
                // Boolean literals must use Python's capitalized True/False (LimeValue.Literal.toString()
                // returns the lowercase "true"/"false" used by most LIME targets).
                if (actualType is LimeBasicType && actualType.typeId == LimeBasicType.TypeId.BOOLEAN) {
                    when (limeValue.value) {
                        "true" -> "True"
                        "false" -> "False"
                        else -> limeValue.value
                    }
                } else {
                    limeValue.toString()
                }
            }
            else -> limeValue.toString()
        }

    /**
     * Resolves a unique C++ function name for the per-type `register_*` function emitted by each
     * pybind11 translation unit. The name includes the LIME package path (e.g. `test_StructConstants`)
     * so that two types with the same short name in different packages (e.g. `test.StructConstants` and
     * `fire.StructConstants`) do not collide at link time.
     */
    fun resolveRegisterName(limeElement: LimeNamedElement): String {
        val name = nameRules.getFlattenedName(limeElement)
        val packagePath = limeElement.path.head.joinToString("_")
        return if (packagePath.isNotEmpty()) "${packagePath}_$name" else name
    }

    private fun getPlatformName(limeElement: LimeNamedElement): String? = limeElement.attributes.get(PYTHON, NAME)
}
