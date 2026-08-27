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

import com.here.gluecodium.cli.GluecodiumExecutionException
import com.here.gluecodium.common.LimeLogger
import com.here.gluecodium.generator.common.CommentsProcessor
import com.here.gluecodium.generator.common.NameResolver
import com.here.gluecodium.generator.common.ReferenceMapBasedResolver
import com.here.gluecodium.model.lime.LimeAttributeType.JS
import com.here.gluecodium.model.lime.LimeAttributeValueType.NAME
import com.here.gluecodium.model.lime.LimeBasicType
import com.here.gluecodium.model.lime.LimeComment
import com.here.gluecodium.model.lime.LimeElement
import com.here.gluecodium.model.lime.LimeFunction
import com.here.gluecodium.model.lime.LimeLambda
import com.here.gluecodium.model.lime.LimeList
import com.here.gluecodium.model.lime.LimeMap
import com.here.gluecodium.model.lime.LimeNamedElement
import com.here.gluecodium.model.lime.LimeReturnType
import com.here.gluecodium.model.lime.LimeSet
import com.here.gluecodium.model.lime.LimeType
import com.here.gluecodium.model.lime.LimeTypeAlias
import com.here.gluecodium.model.lime.LimeTypeRef

/**
 * Main name resolver for the JS generator. Resolves TypeScript type names for LIME types and
 * type references, used by the `.d.ts` stub templates. Type names are resolved as own
 * (unqualified) names; nested types are qualified through their parent chain when referenced
 * from outside their declaring container.
 */
internal class JsNameResolver(
    limeReferenceMap: Map<String, LimeElement>,
    private val nameRules: JsNameRules,
    private val limeLogger: LimeLogger,
    private val commentsProcessor: CommentsProcessor,
) : ReferenceMapBasedResolver(limeReferenceMap), NameResolver {
    override fun resolveName(element: Any): String = resolveType(element)

    private val limeToJsNames: Map<String, String> = buildPathMap()

    private fun resolveType(element: Any): String =
        when (element) {
            is LimeComment -> resolveComment(element)
            is LimeBasicType -> resolveBasicType(element)
            is LimeReturnType -> resolveType(element.typeRef)
            is LimeTypeRef -> {
                val actualType = element.type.actualType
                val typeName =
                    when {
                        actualType is LimeBasicType -> resolveBasicType(actualType)
                        actualType is LimeLambda -> resolveLambdaType(actualType)
                        actualType is LimeTypeAlias -> resolveType(actualType.typeRef)
                        actualType is LimeList -> resolveType(actualType)
                        actualType is LimeMap -> resolveType(actualType)
                        actualType is LimeSet -> resolveType(actualType)
                        actualType.path.hasParent -> resolveQualifiedTypeName(actualType)
                        else -> nameRules.getName(actualType)
                    }
                if (element.isNullable) "$typeName | null" else typeName
            }
            is LimeList -> {
                val elementType = resolveType(element.elementType)
                if (element.elementType.isNullable) "Array<$elementType>" else "Array<$elementType>"
            }
            is LimeSet -> "Set<${resolveType(element.elementType)}>"
            is LimeMap ->
                "Map<${resolveType(element.keyType)}, ${resolveType(element.valueType)}>"
            is LimeType -> nameRules.getName(element)
            is LimeNamedElement -> getPlatformName(element) ?: nameRules.getName(element)
            else -> throw GluecodiumExecutionException("Unsupported element type ${element.javaClass.name}")
        }

    private fun resolveComment(limeComment: LimeComment): String {
        val commentText = limeComment.getFor("Js")
        if (commentText.isBlank()) return ""
        val commentedElement =
            limeReferenceMap[limeComment.path.toString()] as? LimeNamedElement
                ?: getParentElement(limeComment.path)
        return commentsProcessor.process(commentedElement.fullName, commentText, limeToJsNames, limeLogger)
    }

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

    private fun buildPathMap(): Map<String, String> =
        limeReferenceMap.values
            .filterIsInstance<LimeNamedElement>()
            .associateBy({ it.path.toAmbiguousString() }, { resolveFullName(it) })

    private fun resolveBasicType(limeBasicType: LimeBasicType): String =
        when (limeBasicType.typeId) {
            LimeBasicType.TypeId.VOID -> "void"
            LimeBasicType.TypeId.BOOLEAN -> "boolean"
            LimeBasicType.TypeId.STRING -> "string"
            LimeBasicType.TypeId.BLOB -> "Uint8Array"
            LimeBasicType.TypeId.FLOAT, LimeBasicType.TypeId.DOUBLE -> "number"
            // 64-bit integers map to bigint (requires -sWASM_BIGINT=1 at link time).
            LimeBasicType.TypeId.INT64, LimeBasicType.TypeId.UINT64 -> "bigint"
            LimeBasicType.TypeId.DATE -> "Date"
            LimeBasicType.TypeId.DURATION -> "bigint"
            LimeBasicType.TypeId.LOCALE -> "string"
            else -> "number"
        }

    private fun resolveLambdaType(limeLambda: LimeLambda): String {
        val function = limeLambda.asFunction()
        val parameters = function.parameters.joinToString(", ") { resolveType(it.typeRef) }
        return "($parameters) => ${resolveType(function.returnType)}"
    }

    /**
     * Resolves the fully-qualified TS name for a nested type (e.g. `Outer.Inner`). Top-level
     * types resolve to their short name.
     */
    private fun resolveQualifiedTypeName(limeType: LimeType): String {
        if (!limeType.path.hasParent) return nameRules.getName(limeType)
        val parentElement = getParentElement(limeType)
        val parentName =
            if (parentElement is LimeType && parentElement.path.hasParent) {
                resolveQualifiedTypeName(parentElement)
            } else {
                nameRules.getName(parentElement)
            }
        return "$parentName.${nameRules.getName(limeType)}"
    }

    override fun resolveReferenceName(element: Any): String? {
        val limeType =
            when (element) {
                is LimeTypeRef -> element.type.actualType
                is LimeType -> element.actualType
                else -> return null
            }
        val namedType = limeType as? LimeType ?: return null
        return resolveQualifiedTypeName(namedType)
    }

    private fun getPlatformName(limeElement: LimeNamedElement): String? = limeElement.attributes.get(JS, NAME)
}
