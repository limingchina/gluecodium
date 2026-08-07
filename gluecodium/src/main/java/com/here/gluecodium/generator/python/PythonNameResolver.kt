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
import com.here.gluecodium.model.lime.LimeFunction
import com.here.gluecodium.model.lime.LimeLambda
import com.here.gluecodium.model.lime.LimeList
import com.here.gluecodium.model.lime.LimeMap
import com.here.gluecodium.model.lime.LimeNamedElement
import com.here.gluecodium.model.lime.LimeParameter
import com.here.gluecodium.model.lime.LimeProperty
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

    /**
     * Pre-built map from LIME element paths (ambiguous strings) to fully-qualified Python names.
     * Used by [resolveComment] to resolve documentation cross-references (Markdown `[ref]` links)
     * to Python-qualified names (e.g. `Comments.SomeStruct`, `Comments.some_method`).
     *
     * Mirrors the `buildPathMap()` pattern used by the Swift, Dart, Kotlin, and Java generators.
     */
    private val limeToPythonNames: Map<String, String> = buildPathMap()

    /**
     * Thread-local context element used during template rendering to resolve constant values
     * that reference nested types. Set by the generator before rendering a class/struct body
     * and cleared afterwards. When set, [resolveValue] uses the short name for same-top-level
     * references and the qualified name for cross-file references.
     */
    private val currentContext: ThreadLocal<LimeNamedElement?> = ThreadLocal()

    /**
     * Per-file map from module path to import alias, for types whose short name clashes with
     * another imported type. Set by the generator before rendering a file and cleared afterwards.
     * When non-empty, [resolvePythonType] and [resolveQualifiedTypeName] substitute the alias
     * for the short name so that runtime references (e.g. `_wrap(..., TypeName)`) resolve to
     * the correct class object.
     */
    private val clashAliases: ThreadLocal<Map<String, String>> = ThreadLocal.withInitial { emptyMap() }

    fun setContext(element: LimeNamedElement?) {
        currentContext.set(element)
    }

    fun clearContext() {
        currentContext.set(null)
    }

    fun setClashAliases(aliases: Map<String, String>) {
        clashAliases.set(aliases)
    }

    fun clearClashAliases() {
        clashAliases.set(emptyMap())
    }

    /**
     * Resolves the name for a top-level type, substituting the clash alias if one is set for
     * this file. Returns the short name when no alias is applicable (the common case).
     */
    private fun resolveTopLevelTypeName(element: LimeNamedElement): String {
        val canonicalElement =
            if (element is LimeType) canonicalizeNamedElement(element) else element
        val modulePath = (canonicalElement.path.head + nameRules.getName(canonicalElement)).joinToString(".")
        return clashAliases.get()[modulePath] ?: nameRules.getName(canonicalElement)
    }

    /**
     * Resolves a type against the filtered model used for Python generation. Type references can
     * retain an element from a duplicate Lime path that was removed by platform filtering, while
     * the filtered reference map points to the element that is actually emitted. Using the
     * filtered element keeps imports, annotations, and wrapper runtime references consistent.
     */
    private fun canonicalizeNamedElement(element: LimeNamedElement): LimeNamedElement =
        (limeReferenceMap[element.path.toString()] as? LimeNamedElement)
            ?: (limeReferenceMap[element.path.toAmbiguousString()] as? LimeNamedElement)
            ?: element

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
                        ?: if (actualType is LimeTypeAlias) {
                            resolvePythonType(actualType.typeRef, requiresHashable)
                        } else if (actualType.path.hasParent) {
                            resolveQualifiedTypeName(actualType)
                        } else {
                            resolvePythonType(actualType, requiresHashable)
                        }
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
            is LimeType -> resolveTopLevelTypeName(element)
            is LimeNamedElement -> getPlatformName(element) ?: resolveTopLevelTypeName(element)
            is LimeValue -> resolveValue(element)
            else -> throw GluecodiumExecutionException("Unsupported element type ${element.javaClass.name}")
        }

    private fun resolveComment(limeComment: LimeComment): String {
        val commentText = limeComment.getFor("Python")
        if (commentText.isBlank()) return ""
        val commentedElement =
            limeReferenceMap[limeComment.path.toString()] as? LimeNamedElement
                ?: getParentElement(limeComment.path)
        return commentsProcessor.process(commentedElement.fullName, commentText, limeToPythonNames, limeLogger)
    }

    /**
     * Resolves the fully-qualified Python name for an element, including parent qualifiers for
     * nested elements (e.g. `Comments.SomeStruct`, `Comments.some_method`). Top-level elements
     * resolve to their short name. Used by [buildPathMap] to populate the documentation
     * cross-reference map.
     *
     * For constructors, the parent class's fully-qualified name is returned directly (since
     * Python constructors are `__init__`, the class name is the most useful reference for
     * documentation).
     */
    private fun resolveFullName(limeElement: LimeNamedElement): String {
        if (!limeElement.path.hasParent) {
            return nameRules.getName(limeElement)
        }
        val parentElement = getParentElement(limeElement)
        if (limeElement is LimeFunction && limeElement.isConstructor) {
            return resolveFullName(parentElement)
        }
        return "${resolveFullName(parentElement)}.${nameRules.getName(limeElement)}"
    }

    /**
     * Builds a map from LIME element paths (as ambiguous strings) to fully-qualified Python names,
     * used for resolving documentation cross-references. Covers all named elements (types,
     * functions, properties, fields, constants, enumerators, parameters, exceptions, lambdas).
     *
     * Property getter/setter function entries are overwritten by the corresponding property's
     * `.get`/`.set` suffix entries (which map to the property name, not the accessor function name).
     *
     * Function signature keys (e.g. `path(Type,Type)`) are also added for overloaded function
     * references.
     */
    private fun buildPathMap(): Map<String, String> {
        val result =
            limeReferenceMap.values
                .filterIsInstance<LimeNamedElement>()
                .filterNot { it is LimeParameter }
                .associateBy({ it.path.toAmbiguousString() }, { resolveFullName(it) })
                .toMutableMap()

        result +=
            limeReferenceMap.values.filterIsInstance<LimeParameter>()
                .associateBy({ it.fullName }, { resolveFullName(it) })

        val functions = limeReferenceMap.values.filterIsInstance<LimeFunction>()
        result += functions.associateBy({ it.path.toAmbiguousString() }, { resolveFullName(it) })
        result +=
            functions.associateBy(
                { function ->
                    function.path.toAmbiguousString() +
                        function.parameters.joinToString(prefix = "(", postfix = ")", separator = ",") { it.typeRef.toString() }
                },
                { resolveFullName(it) },
            )

        val properties = limeReferenceMap.values.filterIsInstance<LimeProperty>()
        result += properties.associateBy({ it.path.toAmbiguousString() + ".get" }, { resolveFullName(it) })
        result +=
            properties.filter { it.setter != null }
                .associateBy({ it.path.toAmbiguousString() + ".set" }, { resolveFullName(it) })

        return result
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
        if (!limeType.path.hasParent) return resolveTopLevelTypeName(limeType)
        // Walk the path tail, looking up each ancestor in the reference map and resolving
        // its (short) name. This produces a dotted qualified name like `Outer.Inner`.
        // For the first component (the top-level type), substitute the clash alias if set.
        val head = limeType.path.head
        val tail = limeType.path.tail
        val sb = StringBuilder()
        var currentFullPath: String? = null
        for ((index, component) in tail.withIndex()) {
            currentFullPath =
                if (currentFullPath == null) {
                    if (head.isNotEmpty()) {
                        head.joinToString(".") + "." + component
                    } else {
                        component
                    }
                } else {
                    "$currentFullPath.$component"
                }
            val element = limeReferenceMap[currentFullPath] as? LimeNamedElement
            val name =
                if (element != null) {
                    if (index == 0) resolveTopLevelTypeName(element) else nameRules.getName(element)
                } else {
                    component
                }
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
            val parent =
                limeReferenceMap[current.path.parent.toString()] as? LimeNamedElement
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
                val parentName =
                    if (parentElement is LimeType && parentElement.path.hasParent) {
                        val ctx = currentContext.get()
                        if (ctx != null && isSameTopLevel(parentElement, ctx)) {
                            nameRules.getName(parentElement)
                        } else {
                            resolveQualifiedTypeName(parentElement)
                        }
                    } else {
                        resolveName(parentElement)
                    }
                "$parentName.${resolveName(limeElement)}"
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

    /**
     * Resolves the Python-side access path for the pybind11-bound type. This is the dotted
     * path used by Python wrapper code to access the native (pybind11-registered) type via
     * `{{nativeModule}}.{{typeName}}`.
     *
     * - Top-level type: `"smoke_OuterClass"` (same as [resolveRegisterName])
     * - Nested type: `"smoke_OuterClass.InnerClass.InnerInnerClass"`
     *
     * With Option B (one pybind11 file per top element with nested scopes), nested types are
     * registered as attributes of their parent `py::class_`, so the access path follows the
     * nesting hierarchy rather than using a flattened name.
     */
    fun resolvePybind11AccessPath(limeElement: LimeNamedElement): String {
        val topLevel = findTopLevelElement(limeElement)
        val topRegName = resolveRegisterName(topLevel)
        if (limeElement.path.toString() == topLevel.path.toString()) return topRegName

        val limeType =
            limeElement as? LimeType
                ?: throw GluecodiumExecutionException("Expected LimeType, got ${limeElement.javaClass.name}")
        val qualifiedName = resolveQualifiedTypeName(limeType)
        // resolveQualifiedTypeName returns "OuterClass.InnerClass" — strip the first component
        // (the top-level name) and prepend the register name.
        val parts = qualifiedName.split(".")
        val pathFromTop = parts.drop(1).joinToString(".")
        return if (pathFromTop.isNotEmpty()) "$topRegName.$pathFromTop" else topRegName
    }

    /**
     * Resolves the short name for pybind11 registration of a type — the string passed as the
     * second argument to `py::class_`/`py::enum_`/`py::exception`.
     *
     * - Top-level type: same as [resolveRegisterName] (e.g. `"smoke_OuterClass"`)
     * - Nested type: just the short name (e.g. `"InnerClass"`)
     */
    fun resolvePybind11ShortName(limeElement: LimeNamedElement): String {
        if (!limeElement.path.hasParent) return resolveRegisterName(limeElement)
        return nameRules.getName(limeElement)
    }

    /**
     * Resolves the register name of the top-level ancestor of [limeElement]. Used by the module
     * init's topological sort to map per-type inheritance dependencies to per-top-level-register
     * dependencies (since nested types are registered within their parent's register function).
     */
    fun resolveTopLevelRegisterName(limeElement: LimeNamedElement): String {
        val topLevel = findTopLevelElement(limeElement)
        return resolveRegisterName(topLevel)
    }

    /**
     * Resolves a chain of pybind11 `.attr("...")` calls to access a (possibly nested) Python class
     * from C++ via an imported module. For a top-level type, this produces:
     * `.attr("TypeName")`
     * For a nested type, this produces:
     * `.attr("ParentName").attr("ChildName")...`
     *
     * Used by the Pybind11Exception template to locate the Python exception class at runtime.
     */
    fun resolvePybind11AttrChain(limeElement: LimeNamedElement): String {
        val qualifiedName =
            resolveQualifiedTypeName(
                limeElement as? LimeType
                    ?: throw GluecodiumExecutionException("Expected LimeType, got ${limeElement.javaClass.name}"),
            )
        return qualifiedName.split(".").joinToString("") { ".attr(\"$it\")" }
    }

    /**
     * Resolves the type expression for a type alias or lambda *definition* (the right-hand
     * side of `Name = <type>`), using **short** (unqualified) names for nested types that
     * belong to the same top-level element as [contextElement]. Types from other top-level
     * elements use their fully-qualified name (e.g. `Outer.Inner`).
     *
     * Inside a class body, the class name itself is not yet defined, so qualified names like
     * `Outer.Inner` fail with `NameError` at runtime. Using the short name `Inner` works
     * because it resolves to the local class-body scope (as long as the referenced type is
     * defined earlier in the body — ensured by reordering in `generateNestedTypeBodies`).
     */
    fun resolveShortTypeRef(
        typeRef: LimeTypeRef,
        contextElement: LimeNamedElement? = null,
    ): String = resolvePythonTypeShort(typeRef, contextElement = contextElement)

    private fun resolvePythonTypeShort(
        element: Any,
        requiresHashable: Boolean = false,
        contextElement: LimeNamedElement? = null,
    ): String =
        when (element) {
            is LimeBasicType -> resolveBasicType(element)
            is LimeReturnType -> resolvePythonTypeShort(element.typeRef, requiresHashable, contextElement)
            is LimeTypeRef -> {
                val actualType = element.type.actualType
                val typeName =
                    (actualType as? LimeLambda)
                        ?.let(::resolveLambdaType)
                        ?: if (actualType is LimeTypeAlias) {
                            resolvePythonTypeShort(actualType.typeRef, requiresHashable, contextElement)
                        } else if (isSameTopLevel(actualType, contextElement)) {
                            nameRules.getName(actualType)
                        } else if (actualType.path.hasParent) {
                            resolveQualifiedTypeName(actualType)
                        } else {
                            resolvePythonTypeShort(actualType, requiresHashable, contextElement)
                        }
                if (element.isNullable) "Optional[" + typeName + "]" else typeName
            }
            is LimeList -> {
                val elementType = resolvePythonTypeShort(element.elementType, requiresHashable, contextElement)
                if (requiresHashable) "tuple[" + elementType + ", ...]" else "list[" + elementType + "]"
            }
            is LimeSet -> {
                val elementType = resolvePythonTypeShort(element.elementType, true, contextElement)
                if (requiresHashable) "frozenset[" + elementType + "]" else "set[" + elementType + "]"
            }
            is LimeMap -> {
                val keyType = resolvePythonTypeShort(element.keyType, true, contextElement)
                val valueType = resolvePythonTypeShort(element.valueType, requiresHashable, contextElement)
                if (requiresHashable) {
                    "frozenset[tuple[" + keyType + ", " + valueType + "]]"
                } else {
                    "dict[" + keyType + ", " + valueType + "]"
                }
            }
            is LimeTypeAlias -> resolvePythonTypeShort(element.typeRef, requiresHashable, contextElement)
            is LimeType -> resolveTopLevelTypeName(element)
            is LimeNamedElement -> getPlatformName(element) ?: resolveTopLevelTypeName(element)
            else -> resolvePythonType(element, requiresHashable)
        }

    /**
     * Returns true if [type] and [context] belong to the same top-level LIME element
     * (i.e. they share the same top-level ancestor in the path hierarchy).
     */
    private fun isSameTopLevel(
        type: LimeType,
        context: LimeNamedElement?,
    ): Boolean {
        if (context == null) return false
        val typeTop = findTopLevelElement(type as LimeNamedElement)
        val contextTop = findTopLevelElement(context)
        return typeTop.path.toString() == contextTop.path.toString()
    }

    private fun getPlatformName(limeElement: LimeNamedElement): String? = limeElement.attributes.get(PYTHON, NAME)
}
