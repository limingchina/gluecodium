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

import com.here.gluecodium.generator.common.Include
import com.here.gluecodium.model.lime.LimeBasicType
import com.here.gluecodium.model.lime.LimeContainer
import com.here.gluecodium.model.lime.LimeException
import com.here.gluecodium.model.lime.LimeEnumeration
import com.here.gluecodium.model.lime.LimeGenericType
import com.here.gluecodium.model.lime.LimeList
import com.here.gluecodium.model.lime.LimeLambda
import com.here.gluecodium.model.lime.LimeMap
import com.here.gluecodium.model.lime.LimeModel
import com.here.gluecodium.model.lime.LimeNamedElement
import com.here.gluecodium.model.lime.LimeSet
import com.here.gluecodium.model.lime.LimeStruct
import com.here.gluecodium.model.lime.LimeType
import com.here.gluecodium.model.lime.LimeTypeRef
import com.here.gluecodium.model.lime.LimeAttributeType

internal class JsGenericRegistrationCollector(
    private val referenceMap: Map<String, com.here.gluecodium.model.lime.LimeElement>,
    private val cppNameRules: com.here.gluecodium.generator.cpp.CppNameRules,
    private val internalNamespace: List<String>,
    private val embindNameResolver: EmbindNameResolver,
    private val requiresJsAdapter: (LimeTypeRef) -> Boolean,
    private val collectEmbindTypes: (LimeType) -> List<LimeType>,
) {
    data class Registrations(
        val entries: List<Map<String, Any>>,
        val includes: List<Map<String, Any>>,
    )

    fun collect(filteredModel: LimeModel): Registrations {
        val registrations = linkedMapOf<String, Map<String, Any>>()
        val includes = linkedSetOf<Include>()
        val includeResolver = EmbindIncludeResolver(referenceMap, cppNameRules, internalNamespace)

        fun collect(typeRef: LimeTypeRef, forceNativeRegistration: Boolean = false) {
            includes += includeResolver.resolveElementImports(typeRef)
            when (val type = typeRef.type) {
                is LimeList -> {
                    collect(type.elementType, forceNativeRegistration)
                    if (forceNativeRegistration || !requiresJsAdapter(typeRef) ||
                        (typeRef.isNullable && !requiresJsAdapter(type.elementType))
                    ) {
                        val elementType = embindNameResolver.resolveName(type.elementType)
                        val name = "Vector_${sanitizeRegistrationName(elementType)}"
                        registrations.putIfAbsent(name, mapOf("vector" to true, "type" to elementType, "name" to name))
                    }
                }
                is LimeMap -> {
                    collect(type.keyType)
                    collect(type.valueType)
                }
                is LimeSet -> collect(type.elementType)
                is LimeLambda -> {
                    type.parameters.map { it.typeRef }.forEach { collect(it, true) }
                    collect(type.returnType.typeRef, true)
                }
                else -> Unit
            }
            if (needsOptionalRegistration(typeRef, forceNativeRegistration)) {
                val typeName = resolveGenericRegistrationType(typeRef.type)
                val name = "Optional_${sanitizeRegistrationName(typeName)}"
                registrations.putIfAbsent(name, mapOf("optional" to true, "type" to typeName, "name" to name))
            }
        }

        filteredModel.topElements
            .filterIsInstance<LimeType>()
            .flatMap(collectEmbindTypes)
            .forEach { type ->
                (type as? LimeContainer)?.let { container ->
                    container.functions.flatMap { it.parameters.map { parameter -> parameter.typeRef } + it.returnType.typeRef }
                        .forEach(::collect)
                    container.properties.map { it.typeRef }.forEach(::collect)
                    container.constants.map { it.typeRef }.forEach(::collect)
                    container.constructors.flatMap { constructor -> constructor.parameters.map { it.typeRef } }.forEach(::collect)
                    (container as? LimeStruct)?.fields?.map { it.typeRef }?.forEach(::collect)
                }
            }
        return Registrations(
            registrations.values.toList(),
            includes.map { mapOf("fileName" to it.fileName, "isSystem" to it.isSystem) },
        )
    }

    private fun resolveGenericRegistrationType(type: LimeType): String =
        when (type.actualType) {
            is LimeBasicType -> embindNameResolver.resolveName(type)
            is LimeGenericType -> embindNameResolver.resolveName(type)
            is LimeException -> embindNameResolver.resolveName(type)
            else -> embindNameResolver.resolveFullName(type.actualType as LimeNamedElement)
        }

    private fun needsOptionalRegistration(typeRef: LimeTypeRef, forceNativeRegistration: Boolean): Boolean {
        if (!typeRef.isNullable) return false
        if (forceNativeRegistration && typeRef.type.actualType is LimeList) return true
        return when (val type = typeRef.type.actualType) {
            is LimeBasicType -> type.typeId !in setOf(LimeBasicType.TypeId.BLOB, LimeBasicType.TypeId.DATE, LimeBasicType.TypeId.DURATION, LimeBasicType.TypeId.LOCALE)
            is LimeEnumeration -> true
            is LimeStruct -> !isObjectStruct(type)
            is LimeList -> !requiresJsAdapter(type.elementType)
            else -> false
        }
    }

    private fun isObjectStruct(struct: LimeStruct): Boolean =
        struct.attributes.have(LimeAttributeType.IMMUTABLE) || struct.fields.any { field ->
            (field.typeRef.type.actualType as? LimeStruct)?.let(::isObjectStruct) == true
        }

    private fun sanitizeRegistrationName(typeName: String) =
        typeName.replace(Regex("[^A-Za-z0-9_]"), "_").trim('_').ifEmpty { "Type" }
}
