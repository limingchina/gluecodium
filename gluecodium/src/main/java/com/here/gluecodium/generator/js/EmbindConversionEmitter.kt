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
import com.here.gluecodium.generator.cpp.CppNameResolver
import com.here.gluecodium.model.lime.LimeAttributeType
import com.here.gluecodium.model.lime.LimeAttributeType.CPP
import com.here.gluecodium.model.lime.LimeAttributeValueType.ACCESSORS
import com.here.gluecodium.model.lime.LimeBasicType
import com.here.gluecodium.model.lime.LimeClass
import com.here.gluecodium.model.lime.LimeInterface
import com.here.gluecodium.model.lime.LimeLambda
import com.here.gluecodium.model.lime.LimeList
import com.here.gluecodium.model.lime.LimeMap
import com.here.gluecodium.model.lime.LimeParameter
import com.here.gluecodium.model.lime.LimeSet
import com.here.gluecodium.model.lime.LimeStruct
import com.here.gluecodium.model.lime.LimeType
import com.here.gluecodium.model.lime.LimeTypeAlias
import com.here.gluecodium.model.lime.LimeTypeRef
import com.here.gluecodium.model.lime.LimeDirectTypeRef
import com.here.gluecodium.model.lime.LimeBasicType.TypeId

/**
 * Emits the C++ conversion expressions that shuttle values between JavaScript and native code
 * across the embind boundary (`jsToNative` / `nativeToJs` families), plus the type predicates
 * that decide when a value must travel as `emscripten::val` instead of a registered type.
 */
internal class EmbindConversionEmitter(
    private val nameResolver: EmbindNameResolver,
    private val cppNameCache: CppNameCache,
    private val nameRules: JsNameRules,
) {
    fun jsToNative(typeRef: LimeTypeRef, source: String): String {
        if (typeRef.isNullable) {
            val nativeType = nameResolver.resolveName(typeRef)
            val value = jsToNativeNonNullable(typeRef.type.actualType, typeRef, source)
            return "($source.isNull() || $source.isUndefined() ? " +
                "$nativeType{} : $nativeType($value))"
        }
        return jsToNativeNonNullable(typeRef.type.actualType, typeRef, source)
    }

    private fun jsToNativeNonNullable(actualType: LimeType, typeRef: LimeTypeRef, source: String): String =
        when (actualType) {
            is LimeClass, is LimeInterface ->
                "gluecodium_js::shared_ptr_from_js<${cppNameCache.getFullyQualifiedName(actualType)}>($source)"
            is LimeList -> {
                val element = jsToNative(actualType.elementType, "entry")
                "([&]() { ${nameResolver.resolveName(typeRef.type)} converted; " +
                    "for (const auto& entry : $source.call<emscripten::val>(\"values\")) { " +
                    "converted.emplace_back($element); } return converted; }())"
            }
            is LimeMap -> {
                val key = jsToNative(actualType.keyType, "entry[0]")
                val value = jsToNative(actualType.valueType, "entry[1]")
                "([&]() { ${nameResolver.resolveName(typeRef.type)} converted; " +
                    "for (const auto& entry : $source.call<emscripten::val>(\"entries\")) { " +
                    "converted.emplace($key, $value); } return converted; }())"
            }
            is LimeSet -> {
                val element = jsToNative(actualType.elementType, "entry")
                "([&]() { ${nameResolver.resolveName(typeRef.type)} converted; " +
                    "for (const auto& entry : $source.call<emscripten::val>(\"values\")) { " +
                    "converted.emplace($element); } return converted; }())"
            }
            is LimeStruct -> if (isObjectStruct(actualType)) {
                val arguments = actualType.fields.joinToString(", ") { field ->
                    jsToNative(field.typeRef, "$source[\"${nameRules.getName(field)}\"]")
                }
                "${cppNameCache.getFullyQualifiedName(actualType)}($arguments)"
            } else {
                "$source.as<${nameResolver.resolveName(typeRef)}>()"
            }
            is LimeBasicType ->
                if (actualType.typeId == TypeId.DATE && isJsDate(typeRef)) {
                    "gluecodium_date_to_native<${nameResolver.resolveName(typeRef.type)}>( $source )"
                } else if (actualType.typeId == TypeId.LOCALE) {
                    "gluecodium_locale_to_native($source)"
                } else if (actualType.typeId == TypeId.DURATION) {
                    val nativeTypeRef = LimeDirectTypeRef(typeRef.type, false, typeRef.attributes)
                    "gluecodium_duration_to_native<${nameResolver.resolveName(nativeTypeRef)}>( $source )"
                } else if (actualType.typeId == TypeId.BLOB) {
                    "::std::make_shared<::std::vector<uint8_t>>(emscripten::convertJSArrayToNumberVector<uint8_t>($source))"
                } else {
                    "$source.as<${nameResolver.resolveName(typeRef)}>()"
                }
            is LimeLambda -> lambdaAdapterExpression(actualType, source)
            else -> "$source.as<${nameResolver.resolveName(typeRef)}>()"
        }

    private fun lambdaAdapterExpression(lambda: LimeLambda, source: String, captureName: String = "__lambda"): String {
        val function = lambda.asFunction()
        val returnType = nameResolver.resolveName(function.returnType)
        val parameters = function.parameters.map { parameter ->
            val type = nameResolver.resolveName(parameter.typeRef)
            val cppType = if (CppNameResolver.needsRefSuffix(parameter.typeRef)) "const $type&" else type
            "$cppType ${parameter.path.name}"
        }
        val arguments = function.parameters.joinToString(", ") { parameter ->
            nativeToJs(parameter.typeRef, parameter.path.name)
        }
        val invocation = "$captureName->callFunction<$returnType>(${arguments})"
        val body = if (function.returnType.isVoid) {
            "gluecodium_js::invoke_on_main_runtime_thread_void([&] { $invocation; });"
        } else {
            "return gluecodium_js::invoke_on_main_runtime_thread([&] { return $invocation; });"
        }
        val capturedSource = if (source.startsWith("std::move(")) source else "emscripten::val($source)"
        return "[$captureName = std::shared_ptr<gluecodium_js::RuntimeThreadVal>(new gluecodium_js::RuntimeThreadVal($capturedSource), gluecodium_js::delete_runtime_thread_val)](${parameters.joinToString(", ")}) -> $returnType { $body }"
    }

    /** Emits the statement that prepares an adapter parameter before the native call. */
    fun parameterPreparation(parameter: LimeParameter, callName: String): String {
        val typeRef = parameter.typeRef
        return if (needsValParameterAdapter(typeRef)) {
            "auto $callName = ${jsToNative(typeRef, parameter.path.name)};"
        } else {
            ""
        }
    }

    fun nativeToJs(typeRef: LimeTypeRef, source: String): String {
        if (typeRef.isNullable) {
            if (typeRef.type.actualType is LimeClass || typeRef.type.actualType is LimeInterface) {
                return "($source ? emscripten::val($source) : emscripten::val::undefined())"
            }
            return "($source ? ${nativeToJsNonNullable(typeRef.type.actualType, typeRef, "*$source")} : emscripten::val::undefined())"
        }
        return nativeToJsNonNullable(typeRef.type.actualType, typeRef, source)
    }

    private fun nativeToJsNonNullable(actualType: LimeType, typeRef: LimeTypeRef, source: String): String =
        when (actualType) {
            is LimeClass, is LimeInterface ->
                "emscripten::val($source)"
            is LimeList -> {
                val element = nativeToJs(actualType.elementType, "entry")
                "([&]() { auto jsResult = emscripten::val::global(\"Array\").new_(); " +
                    "for (const auto& entry : $source) { jsResult.call<void>(\"push\", $element); } " +
                    "return jsResult; }())"
            }
            is LimeMap -> {
                val key = nativeToJs(actualType.keyType, "entry.first")
                val value = nativeToJs(actualType.valueType, "entry.second")
                "([&]() { auto jsResult = emscripten::val::global(\"Map\").new_(); " +
                    "for (const auto& entry : $source) { jsResult.call<void>(\"set\", $key, $value); } " +
                    "return jsResult; }())"
            }
            is LimeSet -> {
                val element = nativeToJs(actualType.elementType, "entry")
                "([&]() { auto jsResult = emscripten::val::global(\"Set\").new_(); " +
                    "for (const auto& entry : $source) { jsResult.call<void>(\"add\", $element); } " +
                    "return jsResult; }())"
            }
            is LimeStruct -> if (isObjectStruct(actualType)) {
                val fields = actualType.fields.joinToString(" ") { field ->
                    val fieldSource = "($source)"
                    val fieldValue = if (actualType.attributes.have(CPP, ACCESSORS)) {
                        "$fieldSource.${cppNameCache.getGetterName(field)}()"
                    } else {
                        "$fieldSource.${cppNameCache.getName(field)}"
                    }
                    "jsResult.set(\"${nameRules.getName(field)}\", ${nativeToJs(field.typeRef, fieldValue)});"
                }
                "([&]() { auto jsResult = emscripten::val::object(); $fields return jsResult; }())"
            } else {
                "emscripten::val($source)"
            }
            is LimeBasicType ->
                if (actualType.typeId == TypeId.DATE && isJsDate(typeRef)) {
                    "gluecodium_date_to_js($source)"
                } else if (actualType.typeId == TypeId.LOCALE) {
                    "gluecodium_locale_to_js($source)"
                } else if (actualType.typeId == TypeId.DURATION) {
                    "gluecodium_duration_to_js($source)"
                } else if (actualType.typeId == TypeId.BLOB) {
                    "emscripten::val::global(\"Uint8Array\").new_(emscripten::val::array($source ? *$source : ::std::vector<uint8_t>{}))"
                } else {
                    "emscripten::val($source)"
                }
            else -> "emscripten::val($source)"
        }

    /** Emits the return statement converting a native `result` back to JS, if any is needed. */
    fun adapterReturnConversion(returnType: LimeTypeRef): String =
        if (returnsViaVal(returnType)) {
            "return ${nativeToJs(returnType, "result")};"
        } else {
            ""
        }

    fun thrownReturnConversion(errorIsEnum: Boolean, returnIsVoid: Boolean, returnType: LimeTypeRef): String {
        if (errorIsEnum && returnIsVoid) {
            return "auto jsResult = emscripten::val::object(); " +
                "if (result.value() != 0) { jsResult.set(\"error\", result.value()); } " +
                "return jsResult;"
        }
        val errorExpression = if (errorIsEnum) "result.error().value()" else "result.error()"
        val successExpression =
            if (returnIsVoid) "" else " jsResult.set(\"value\", ${nativeToJs(returnType, "result.unsafe_value()")});"
        return "auto jsResult = emscripten::val::object(); " +
            "if (result) {$successExpression} else { jsResult.set(\"error\", $errorExpression); } " +
            "return jsResult;"
    }

    /** Return types whose native `result` must be converted to JS before returning. */
    fun returnsViaVal(returnType: LimeTypeRef): Boolean =
        returnType.isNullable || isJsDate(returnType) || isJsLocale(returnType) ||
            isJsDuration(returnType) || isBlob(returnType) || isObjectStruct(returnType) ||
            returnType.type.actualType is LimeList ||
            returnType.type.actualType is LimeMap ||
            returnType.type.actualType is LimeSet

    /**
     * Non-recursive check used for function parameters: types that cannot pass through
     * embind directly and must travel as `emscripten::val`.
     */
    fun needsValParameterAdapter(typeRef: LimeTypeRef): Boolean {
        if (typeRef.isNullable || isJsDate(typeRef) || isJsLocale(typeRef) ||
            isJsDuration(typeRef) || isBlob(typeRef) || isObjectStruct(typeRef)
        ) return true
        return when (typeRef.type.actualType) {
            is LimeClass, is LimeInterface, is LimeLambda,
            is LimeList, is LimeMap, is LimeSet,
            -> true
            else -> false
        }
    }

    /**
     * Recursive check used for properties and generic registrations: a type requires an
     * adapter if it or any nested generic element type does.
     */
    fun requiresJsAdapter(typeRef: LimeTypeRef): Boolean {
        if (typeRef.isNullable || isJsDate(typeRef) || isJsLocale(typeRef) || isJsDuration(typeRef) || isBlob(typeRef) || isObjectStruct(typeRef)) return true
        return when (val actualType = typeRef.type.actualType) {
            is LimeClass, is LimeInterface -> true
            is LimeList -> requiresJsAdapter(actualType.elementType)
            is LimeMap -> requiresJsAdapter(actualType.keyType) || requiresJsAdapter(actualType.valueType)
            is LimeSet -> requiresJsAdapter(actualType.elementType)
            is LimeLambda -> true
            else -> false
        }
    }

    fun hasCppStringOverride(typeRef: LimeTypeRef): Boolean {
        val actualType = typeRef.type.actualType
        return actualType is LimeBasicType &&
            actualType.typeId == TypeId.STRING &&
            typeRef.attributes.get(CPP, com.here.gluecodium.model.lime.LimeAttributeValueType.TYPE) != null
    }

    fun isBlob(typeRef: LimeTypeRef): Boolean =
        (typeRef.type.actualType as? LimeBasicType)?.typeId == TypeId.BLOB

    fun isObjectStruct(typeRef: LimeTypeRef): Boolean =
        (typeRef.type.actualType as? LimeStruct)?.let(::isObjectStruct) == true

    /** A struct that is immutable or contains object-struct fields cannot be value-copied by embind. */
    fun isObjectStruct(struct: LimeStruct): Boolean =
        struct.attributes.have(LimeAttributeType.IMMUTABLE) ||
            struct.fields.any { isObjectStruct(it.typeRef) }

    fun isJsDate(typeRef: LimeTypeRef): Boolean =
        (typeRef.type.actualType as? LimeBasicType)?.typeId == TypeId.DATE &&
            !hasCppTypeOverride(typeRef)

    fun isJsDuration(typeRef: LimeTypeRef): Boolean =
        (typeRef.type.actualType as? LimeBasicType)?.typeId == TypeId.DURATION

    fun isJsLocale(typeRef: LimeTypeRef): Boolean =
        (typeRef.type.actualType as? LimeBasicType)?.typeId == TypeId.LOCALE

    private fun hasCppTypeOverride(typeRef: LimeTypeRef): Boolean {
        if (typeRef.attributes.have(CPP, com.here.gluecodium.model.lime.LimeAttributeValueType.TYPE)) return true
        val alias = typeRef.type as? LimeTypeAlias ?: return false
        return hasCppTypeOverride(alias.typeRef)
    }
}
