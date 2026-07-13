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
    override fun resolveName(element: Any): String =
        when (element) {
            is LimeComment -> resolveComment(element)
            is LimeBasicType -> resolveBasicType(element)
            is LimeReturnType -> resolveName(element.typeRef)
            is LimeTypeRef -> resolveTypeRefName(element)
            is LimeList -> "list[" + resolveName(element.elementType) + "]"
            is LimeSet -> "set[" + resolveName(element.elementType) + "]"
            is LimeMap -> "dict[" + resolveName(element.keyType) + ", " + resolveName(element.valueType) + "]"
            is LimeTypeAlias -> resolveName(element.typeRef)
            is LimeType -> nameRules.getName(element)
            is LimeNamedElement -> getPlatformName(element) ?: nameRules.getName(element)
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

    private fun resolveTypeRefName(limeTypeRef: LimeTypeRef): String {
        val limeType = limeTypeRef.type
        return if (limeTypeRef.isNullable) "Optional[" + resolveName(limeType) + "]" else resolveName(limeType)
    }

    private fun getPlatformName(limeElement: LimeNamedElement): String? = limeElement.attributes.get(PYTHON, NAME)
}
