/*
 * Copyright (C) 2016-2019 HERE Europe B.V.
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

package com.here.genium.generator.cbridge

import com.here.genium.generator.common.NameHelper
import com.here.genium.model.lime.LimeAttributeType.SWIFT
import com.here.genium.model.lime.LimeAttributeValueType.NAME
import com.here.genium.model.lime.LimeContainer
import com.here.genium.model.lime.LimeElement
import com.here.genium.model.lime.LimeMethod
import com.here.genium.model.lime.LimeNamedElement
import com.here.genium.model.lime.LimeSignatureResolver
import com.here.genium.model.lime.LimeStruct
import com.here.genium.model.lime.LimeType
import java.nio.file.Paths

object CBridgeNameRules {
    const val CBRIDGE_PUBLIC = "cbridge"
    const val CBRIDGE_INTERNAL = "cbridge_internal"
    const val INCLUDE_DIR = "include"

    const val BASE_REF_NAME = "_baseRef"

    const val UNDERSCORE = "_"
    const val PUBLIC_HEADER_SUFFIX = ".h"
    const val IMPL_SUFFIX = ".cpp"
    const val CBRIDGE_PREFIX = "cbridge_"

    val STRING_HANDLE_FILE = Paths.get(CBRIDGE_PUBLIC, INCLUDE_DIR, "StringHandle.h").toString()
    val DATE_HANDLE_FILE = Paths.get(CBRIDGE_PUBLIC, INCLUDE_DIR, "DateHandle.h").toString()
    val BASE_HANDLE_IMPL_FILE =
        Paths.get(CBRIDGE_INTERNAL, INCLUDE_DIR, "BaseHandleImpl.h").toString()
    val BASE_HANDLE_FILE = Paths.get(CBRIDGE_PUBLIC, INCLUDE_DIR, "BaseHandle.h").toString()
    val EXPORT_FILE = Paths.get(CBRIDGE_PUBLIC, INCLUDE_DIR, "Export.h").toString()
    const val SRC_DIR = "src"

    fun getName(limeElement: LimeNamedElement) =
        getPlatformName(limeElement) ?: NameHelper.toUpperCamelCase(limeElement.name)

    fun getFunctionTableName(limeContainer: LimeContainer) =
        getInterfaceName(limeContainer) + "_FunctionTable"

    fun getInterfaceName(limeContainer: LimeContainer) = getNestedSpecifierString(limeContainer)

    fun getShortMethodName(
        limeReferenceMap: Map<String, LimeElement>,
        limeMethod: LimeMethod,
        isOverloaded: Boolean
    ): String {
        val limeParent = limeReferenceMap[limeMethod.path.parent.toString()]
        val prefix = when (limeParent) {
            is LimeStruct -> getName(limeParent) + UNDERSCORE
            else -> ""
        }
        val suffix = when {
            isOverloaded -> {
                val signature = LimeSignatureResolver(limeReferenceMap).getSignature(limeMethod)
                UNDERSCORE + signature.joinToString(UNDERSCORE) { mangleSignature(it) }
            }
            else -> ""
        }
        val methodName = getPlatformName(limeMethod) ?: NameHelper.toLowerCamelCase(limeMethod.name)
        return prefix + methodName + suffix
    }

    private fun mangleSignature(name: String) =
        name.replace("_", "_1").replace(":", "_2").replace("[", "_3").replace("]", "_4")

    private fun joinQualifiedName(nameSpecifier: List<String>, name: String) =
        (nameSpecifier + name).joinToString(UNDERSCORE)

    private fun getNestedNameSpecifier(limeElement: LimeNamedElement) =
        limeElement.path.head + NameHelper.toUpperCamelCase(limeElement.path.container)

    fun getNestedSpecifierString(limeElement: LimeNamedElement) =
        getNestedNameSpecifier(limeElement).joinToString(UNDERSCORE)

    fun getTypeName(limeType: LimeType) =
        joinQualifiedName(getNestedNameSpecifier(limeType), getName(limeType))

    fun getBaseApiCall(category: CppTypeInfo.TypeCategory, baseAPIName: String) =
        if (category === CppTypeInfo.TypeCategory.CLASS)
            "std::shared_ptr<$baseAPIName>"
        else
            baseAPIName

    fun getPropertySetterName(name: String) = NameHelper.toLowerCamelCase(name) + "_set"

    fun getPropertyGetterName(name: String) = NameHelper.toLowerCamelCase(name) + "_get"

    private fun getPlatformName(limeElement: LimeNamedElement?) =
        limeElement?.attributes?.get(SWIFT, NAME, String::class.java)
}
