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
import com.here.gluecodium.generator.cpp.CppNameRules
import com.here.gluecodium.generator.cpp.CppSignatureResolver
import com.here.gluecodium.model.lime.LimeAttributeType.CPP
import com.here.gluecodium.model.lime.LimeAttributeValueType.ACCESSORS
import com.here.gluecodium.model.lime.LimeAttributeValueType.CONST
import com.here.gluecodium.model.lime.LimeAttributeValueType.NOEXCEPT
import com.here.gluecodium.model.lime.LimeBasicType
import com.here.gluecodium.model.lime.LimeClass
import com.here.gluecodium.model.lime.LimeConstant
import com.here.gluecodium.model.lime.LimeContainer
import com.here.gluecodium.model.lime.LimeContainerWithInheritance
import com.here.gluecodium.model.lime.LimeElement
import com.here.gluecodium.model.lime.LimeEnumeration
import com.here.gluecodium.model.lime.LimeException
import com.here.gluecodium.model.lime.LimeExternalDescriptor
import com.here.gluecodium.model.lime.LimeField
import com.here.gluecodium.model.lime.LimeFunction
import com.here.gluecodium.model.lime.LimeInterface
import com.here.gluecodium.model.lime.LimeList
import com.here.gluecodium.model.lime.LimeMap
import com.here.gluecodium.model.lime.LimeModel
import com.here.gluecodium.model.lime.LimeNamedElement
import com.here.gluecodium.model.lime.LimeParameter
import com.here.gluecodium.model.lime.LimeProperty
import com.here.gluecodium.model.lime.LimeSet
import com.here.gluecodium.model.lime.LimeStruct
import com.here.gluecodium.model.lime.LimeType
import com.here.gluecodium.model.lime.LimeTypeRef

internal class JsEmbindViewModelBuilder(
    private val internalNamespace: List<String>,
    private val referenceMap: Map<String, LimeElement>,
    private val nameRules: JsNameRules,
    private val cppNameRules: CppNameRules,
    private val embindNameResolver: EmbindNameResolver,
    private val cppNameCache: CppNameCache,
    private val conversions: EmbindConversionEmitter,
    private val resolveRegisterName: (LimeNamedElement) -> String,
    private val primaryBaseType: (LimeType, LimeModel) -> LimeContainerWithInheritance?,
    private val secondaryParentMembers: (LimeType, LimeModel) -> Pair<List<LimeFunction>, List<LimeProperty>>,
    private val primaryInheritedOverloads: (LimeType, LimeModel) -> List<LimeFunction>,
    private val isSupportedConstant: (LimeConstant) -> Boolean,
) {
    private val signatureResolver = CppSignatureResolver(referenceMap, cppNameRules)

    fun build(type: LimeType, filteredModel: LimeModel): Map<String, Any> {
        val data = mutableMapOf<String, Any>(
            "model" to type,
            "internalNamespace" to internalNamespace,
            "jsName" to nameRules.getName(type),
            "embindName" to nameRules.getEmbindRuntimeName(type),
            "cppFullName" to cppNameCache.getFullyQualifiedName(type),
            "registerName" to resolveRegisterName(type),
            "isObjectStruct" to (type is LimeStruct && conversions.isObjectStruct(type)),
        )
        primaryBaseType(type, filteredModel)?.let { data["primaryBase"] = cppNameCache.getFullyQualifiedName(it) }
        if (type is LimeEnumeration) {
            val enumerators = type.enumerators.map(::enumeratorViewModel)
            data["enumeratorBindings"] = enumerators.joinToString("\n") {
                "    .value(\"${it["jsName"]}\", ${it["cppName"]})"
            }
        }
        val container = type as? LimeContainer ?: return data
        val (secondaryFunctions, secondaryProperties) = secondaryParentMembers(type, filteredModel)
        if (type is LimeInterface) {
            val inheritedContainer = type as LimeContainerWithInheritance
            data["wrapperName"] = "${resolveRegisterName(type)}Wrapper"
            data["wrapperEmbindName"] = "${nameRules.getEmbindRuntimeName(type)}__Wrapper"
            data["wrapperPtrEmbindName"] = "${nameRules.getEmbindRuntimeName(type)}__WrapperPtr"
            data["wrapperMethods"] =
                (container.functions + inheritedContainer.inheritedFunctions)
                    .filterNot { it.isStatic || it.isConstructor }
                    .distinctBy { it.fullName }
                    .map(::wrapperMethodViewModel)
            data["wrapperProperties"] =
                (container.properties + inheritedContainer.inheritedProperties)
                    .filterNot { it.isStatic }
                    .distinctBy { it.fullName }
                    .map(::wrapperPropertyViewModel)
        }
        data["constructors"] = container.constructors.map { functionViewModel(it) }
        val inheritedOverloads = primaryInheritedOverloads(type, filteredModel)
        data["methods"] =
            (inheritedOverloads + container.functions.filterNot { it.isConstructor } + secondaryFunctions)
                .distinctBy { it.fullName }
                .map {
                    functionViewModel(
                        it,
                        isFlattened = secondaryFunctions.contains(it),
                        flattenedReceiverType = cppNameCache.getFullyQualifiedName(type),
                        isPureVirtual = type is LimeInterface,
                        forceOverloadAdapter = inheritedOverloads.contains(it),
                    )
                }
        data["properties"] =
            (container.properties + secondaryProperties)
                .distinctBy { it.fullName }
                .map(::propertyViewModel)
        if (type is LimeStruct) {
            data["fields"] = type.fields.map { fieldViewModel(type, it) }
            data["structFunctions"] = container.functions
                .filter { it.isStatic && !it.isConstructor }
                .map { functionViewModel(it).toMutableMap().apply { put("runtimeName", structFunctionRuntimeName(it)) } }
        }
        data["constants"] = container.constants.filter(isSupportedConstant).map(::constantViewModel)
        return data
    }

    private fun wrapperMethodViewModel(function: LimeFunction): Map<String, Any> {
        val exception = function.exception
        val errorType = exception?.errorType?.let(embindNameResolver::resolveName)
        val errorActualType = exception?.errorType?.type?.actualType
        val returnType = if (exception != null) {
            val valueType = if (function.returnType.isVoid) "void" else embindNameResolver.resolveName(function.returnType)
            if (errorActualType is LimeEnumeration && function.returnType.isVoid) {
                "::std::error_code"
            } else {
                val nativeErrorType = if (errorActualType is LimeEnumeration) "::std::error_code" else errorType
                "::${internalNamespace.joinToString("::")}::Return<$valueType, $nativeErrorType>"
            }
        } else {
            embindNameResolver.resolveName(function.returnType)
        }
        val returnNeedsAdapter = requiresWrapperJsAdapter(function.returnType.typeRef)
        val parameters = function.parameters.map { parameter ->
            val nativeType = embindNameResolver.resolveName(parameter.typeRef)
            val parameterType =
                if (CppNameResolver.needsRefSuffix(parameter.typeRef)) "const $nativeType&" else nativeType
            "$parameterType ${parameter.path.name}"
        }
        val needsAdapter = returnNeedsAdapter || function.parameters.any { requiresWrapperJsAdapter(it.typeRef) }
        val arguments = function.parameters.joinToString(", ") { parameter ->
            if (needsAdapter) conversions.nativeToJs(parameter.typeRef, parameter.path.name) else parameter.path.name
        }
        val callArguments = if (arguments.isNotEmpty()) ", $arguments" else ""
        val call = if (exception != null) {
            val valueType = if (function.returnType.isVoid) "void" else embindNameResolver.resolveName(function.returnType)
            val helper = when {
                errorActualType is LimeEnumeration && function.returnType.isVoid -> "return_from_js_enum_void"
                errorActualType is LimeEnumeration -> "return_from_js_enum"
                else -> "return_from_js"
            }
            val helperTypes = if (errorActualType is LimeEnumeration && function.returnType.isVoid) {
                errorType
            } else {
                "$valueType, $errorType"
            }
            "gluecodium_js::$helper<$helperTypes>([&] { return call<emscripten::val>(\"${nameRules.getName(function)}\"$callArguments); })"
        } else if (needsAdapter) {
            val jsResult = "call<emscripten::val>(\"${nameRules.getName(function)}\"$callArguments)"
            if (function.returnType.isVoid) "$jsResult;" else "return ${conversions.jsToNative(function.returnType.typeRef, jsResult)};"
        } else {
            "call<$returnType>(\"${nameRules.getName(function)}\"$callArguments)"
        }
        val lambdaCaptures = function.parameters.joinToString(", ") { "&${it.path.name}" }
        val lambdaCaptureList = if (lambdaCaptures.isEmpty()) "this" else "this, $lambdaCaptures"
        val lambdaBody = if (exception != null) {
            "return $call;"
        } else if (needsAdapter) {
            call
        } else if (function.returnType.isVoid) {
            "$call;"
        } else {
            "return $call;"
        }
        val threadedCall = if (function.returnType.isVoid && exception == null) {
            "gluecodium_js::invoke_on_main_runtime_thread_void([${lambdaCaptureList}]() { $lambdaBody });"
        } else {
            "return gluecodium_js::invoke_on_main_runtime_thread([${lambdaCaptureList}]() { $lambdaBody });"
        }
        return mapOf(
            "returnType" to returnType,
            "cppName" to embindNameResolver.resolveName(function),
            "parameters" to parameters.joinToString(", "),
            "call" to call,
            "threadedCall" to threadedCall,
            "isVoid" to function.returnType.isVoid,
            "needsAdapter" to needsAdapter,
            "isConst" to function.attributes.have(CPP, CONST),
            "isNoexcept" to function.attributes.have(CPP, NOEXCEPT),
            "isThrown" to (exception != null),
        )
    }

    private fun requiresWrapperJsAdapter(typeRef: LimeTypeRef): Boolean =
        typeRef.type.actualType is LimeStruct || conversions.needsValParameterAdapter(typeRef)

    private fun wrapperPropertyViewModel(property: LimeProperty): Map<String, Any> {
        val propertyType = embindNameResolver.resolveName(property.typeRef)
        val setterParameter =
            if (CppNameResolver.needsRefSuffix(property.typeRef)) "const $propertyType& value" else "$propertyType value"
        val needsAdapter = conversions.requiresJsAdapter(property.typeRef)
        val getterCall = "get(\"${nameRules.getName(property)}\")"
        val threadedGetter = if (needsAdapter) {
            "return gluecodium_js::invoke_on_main_runtime_thread([this] { return ${conversions.jsToNative(property.typeRef, getterCall)}; });"
        } else {
            "return gluecodium_js::invoke_on_main_runtime_thread([this] { return get(\"${nameRules.getName(property)}\").as<$propertyType>(); });"
        }
        val threadedSetter = if (needsAdapter) {
            "gluecodium_js::invoke_on_main_runtime_thread_void([this, &value] { set(\"${nameRules.getName(property)}\", ${conversions.nativeToJs(property.typeRef, "value")}); });"
        } else {
            "gluecodium_js::invoke_on_main_runtime_thread_void([this, &value] { set(\"${nameRules.getName(property)}\", emscripten::val(value)); });"
        }
        return mapOf(
            "returnType" to propertyType,
            "jsName" to nameRules.getName(property),
            "cppGetterName" to cppNameCache.getGetterName(property),
            "cppSetterName" to cppNameCache.getSetterName(property),
            "setterParameter" to setterParameter,
            "hasSetter" to (property.setter != null),
            "isNoexcept" to property.attributes.have(CPP, NOEXCEPT),
            "threadedGetter" to threadedGetter,
            "threadedSetter" to threadedSetter,
        )
    }

    private fun functionViewModel(
        function: LimeFunction,
        isFlattened: Boolean = false,
        flattenedReceiverType: String? = null,
        isPureVirtual: Boolean = false,
        forceOverloadAdapter: Boolean = false,
    ): Map<String, Any> {
        val context = FunctionViewModelContext(
            function = function,
            isOverloaded = forceOverloadAdapter || isOverloadedInJsBindings(function),
            returnType = function.returnType.typeRef,
            thrownException = function.exception,
        )
        val data = mutableMapOf<String, Any>(
            "model" to function,
            "jsName" to nameRules.getName(function),
            "embindName" to overloadEmbindName(context),
            "cppName" to embindNameResolver.resolveName(function),
            "isConstructor" to function.isConstructor,
            "isStatic" to function.isStatic,
            "needsAdapter" to needsFunctionAdapter(context),
            "adapterReturnType" to if (context.needsValReturn) "emscripten::val" else embindNameResolver.resolveName(context.returnType),
            "isThrown" to context.isThrown,
            "thrownErrorIsEnum" to context.thrownErrorIsEnum,
            "returnIsNullable" to context.returnType.isNullable,
            "returnIsList" to (context.returnActualType is LimeList),
            "returnIsMap" to (context.returnActualType is LimeMap),
            "isOverloaded" to context.isOverloaded,
            "isFlattened" to isFlattened,
            "isPureVirtual" to isPureVirtual,
            "parameters" to function.parameters.mapIndexed { index, parameter ->
                parameterViewModel(parameter, index == function.parameters.lastIndex)
            },
        )
        data.putAll(adapterViewModel(context))
        if (isFlattened) data.putAll(flattenedViewModel(context, flattenedReceiverType, adapterParameterTypes(function)))
        return data
    }

    private inner class FunctionViewModelContext(
        val function: LimeFunction,
        val isOverloaded: Boolean,
        val returnType: LimeTypeRef,
        val thrownException: LimeException?,
    ) {
        val isExternal: Boolean =
            (referenceMap[function.path.parent.toString()] as? LimeNamedElement)?.external?.cpp != null
        val returnActualType: LimeType = returnType.type.actualType
        val isThrown: Boolean = thrownException != null
        val thrownErrorIsEnum: Boolean = thrownException?.errorType?.type?.actualType is LimeEnumeration
        val needsValReturn: Boolean = isThrown || conversions.returnsViaVal(returnType)
    }

    private fun overloadEmbindName(context: FunctionViewModelContext): String {
        val function = context.function
        return if (context.isOverloaded && (function.isStatic && isJsOverloaded(function) || !function.isStatic)) {
            overloadRuntimeName(function)
        } else {
            nameRules.getName(function)
        }
    }

    private fun needsFunctionAdapter(context: FunctionViewModelContext): Boolean =
        context.isExternal || context.isOverloaded || context.isThrown || conversions.returnsViaVal(context.returnType) ||
            context.function.parameters.any { conversions.hasCppStringOverride(it.typeRef) || conversions.needsValParameterAdapter(it.typeRef) }

    private fun parameterViewModel(parameter: LimeParameter, last: Boolean): Map<String, Any?> {
        val actualType = parameter.typeRef.type.actualType
        return mapOf(
            "model" to parameter,
            "jsName" to nameRules.getName(parameter),
            "cppType" to embindNameResolver.resolveName(parameter.typeRef),
            "adapterType" to if (conversions.hasCppStringOverride(parameter.typeRef)) "::std::string" else if (conversions.needsValParameterAdapter(parameter.typeRef)) "emscripten::val" else embindNameResolver.resolveName(parameter.typeRef),
            "nativeName" to parameter.path.name,
            "nativeType" to embindNameResolver.resolveName(parameter.typeRef),
            "underlyingType" to embindNameResolver.resolveName(parameter.typeRef.type),
            "isNullable" to parameter.typeRef.isNullable,
            "isList" to (actualType is LimeList),
            "isMap" to (actualType is LimeMap),
            "mapKeyType" to (actualType as? LimeMap)?.let { embindNameResolver.resolveName(it.keyType) },
            "mapValueType" to (actualType as? LimeMap)?.let { embindNameResolver.resolveName(it.valueType) },
            "last" to last,
        )
    }

    private class AdapterParameter(val type: String, val name: String, val callName: String, val preparation: String)

    private fun adapterParameters(function: LimeFunction): List<AdapterParameter> =
        function.parameters.map { parameter ->
            val type = if (conversions.hasCppStringOverride(parameter.typeRef)) "::std::string" else if (conversions.needsValParameterAdapter(parameter.typeRef)) "emscripten::val" else embindNameResolver.resolveName(parameter.typeRef)
            val callName = if (conversions.hasCppStringOverride(parameter.typeRef)) "${parameter.path.name}.c_str()" else if (conversions.needsValParameterAdapter(parameter.typeRef)) "${parameter.path.name}_value" else parameter.path.name
            AdapterParameter(type, parameter.path.name, callName, conversions.parameterPreparation(parameter, callName))
        }

    private fun adapterParameterTypes(function: LimeFunction): List<String> = adapterParameters(function).map { it.type }

    private fun adapterViewModel(context: FunctionViewModelContext): Map<String, Any> {
        val parameters = adapterParameters(context.function)
        return mapOf(
            "adapterParameters" to parameters.joinToString(", ") { "${it.type} ${it.name}" },
            "hasAdapterParameters" to parameters.isNotEmpty(),
            "adapterSignatureParameters" to parameters.joinToString(", ") { it.type }.let { if (it.isEmpty()) "void" else it },
            "adapterCallArguments" to parameters.joinToString(", ") { it.callName },
            "adapterPolicies" to rawPointerPolicies(parameters) { it },
            "hasAdapterPolicies" to hasRawPointer(parameters),
            "adapterMemberPolicies" to rawPointerPolicies(parameters) { it + 1 },
            "hasAdapterMemberPolicies" to hasRawPointer(parameters),
            "adapterPreparations" to parameters.map { it.preparation }.filter { it.isNotEmpty() }.joinToString("\n"),
            "adapterCallPrefix" to if (context.needsValReturn) "auto result = " else "return ",
            "adapterReturnConversion" to if (context.isThrown) conversions.thrownReturnConversion(context.thrownErrorIsEnum, context.function.returnType.isVoid, context.returnType) else conversions.adapterReturnConversion(context.returnType),
        )
    }

    private fun rawPointerPolicies(parameters: List<AdapterParameter>, argIndex: (Int) -> Int): String =
        parameters.mapIndexedNotNull { index, parameter ->
            if (parameter.type.endsWith("*")) "allow_raw_pointer<arg<${argIndex(index)}>>()" else null
        }.joinToString(", ")

    private fun hasRawPointer(parameters: List<AdapterParameter>): Boolean = parameters.any { it.type.endsWith("*") }

    private fun flattenedViewModel(
        context: FunctionViewModelContext,
        flattenedReceiverType: String?,
        parameterTypes: List<String>,
    ): Map<String, Any> {
        val receiverType = flattenedReceiverType ?: error("Missing flattened receiver type")
        val returnType = if (context.needsValReturn) "emscripten::val" else embindNameResolver.resolveName(context.returnType)
        return mapOf(
            "flattenedFunctionSignature" to listOf("$returnType($receiverType*", *parameterTypes.toTypedArray()).joinToString(", ").let { "$it)" },
            "flattenedLambdaParameters" to listOf("$receiverType* self", *parameterTypes.zip(context.function.parameters) { type, parameter -> "$type ${parameter.path.name}" }.toTypedArray()).joinToString(", "),
        )
    }

    private fun propertyViewModel(property: LimeProperty): Map<String, Any> =
        run {
            val owner = (referenceMap[property.path.parent.toString()] as? LimeNamedElement)
            val needsAdapter = conversions.requiresJsAdapter(property.typeRef) || owner?.external?.cpp != null
            val getterSource = if (property.isStatic) {
                "${cppNameCache.getFullyQualifiedName(owner as LimeNamedElement)}::${cppNameCache.getGetterName(property)}()"
            } else if (owner?.external?.cpp != null) {
                "const_cast<${cppNameCache.getFullyQualifiedName(owner)}&>(self).${cppNameCache.getGetterName(property)}()"
            } else {
                "self.${cppNameCache.getGetterName(property)}()"
            }
            val adapterGetter = if (needsAdapter) {
                "([&]() { auto result = $getterSource; return ${conversions.nativeToJs(property.typeRef, "result")}; }())"
            } else {
                conversions.nativeToJs(property.typeRef, getterSource)
            }
            mapOf(
                "model" to property,
                "jsName" to nameRules.getName(property),
                "cppGetterName" to cppNameCache.getGetterName(property),
                "cppSetterName" to cppNameCache.getSetterName(property),
                "isStatic" to property.isStatic,
                "hasSetter" to (property.setter != null),
                "cppFullName" to (owner?.let(cppNameCache::getFullyQualifiedName) ?: ""),
                "needsAdapter" to needsAdapter,
                "adapterGetterName" to propertyAdapterName(property, "get"),
                "adapterSetterName" to propertyAdapterName(property, "set"),
                "adapterGetter" to adapterGetter,
                "adapterSetter" to conversions.jsToNative(property.typeRef, "value").let { converted -> if (property.isStatic) "${cppNameCache.getFullyQualifiedName(owner as LimeNamedElement)}::${cppNameCache.getSetterName(property)}($converted)" else "self.${cppNameCache.getSetterName(property)}($converted)" },
            )
        }

    private fun fieldViewModel(struct: LimeStruct, field: LimeField): Map<String, Any?> {
        val cppType = embindNameResolver.resolveName(field.typeRef)
        val hasAccessors = struct.attributes.have(CPP, ACCESSORS) || field.external?.cpp?.get(LimeExternalDescriptor.Companion.GETTER_NAME_NAME) != null
        val hasExternalGetter = field.external?.cpp?.get(LimeExternalDescriptor.Companion.GETTER_NAME_NAME) != null
        val accessorType = if (hasExternalGetter) cppType else if (CppNameResolver.needsRefSuffix(field.typeRef)) "const $cppType&" else cppType
        val directSource = if (hasAccessors) "self.${cppNameCache.getGetterName(field)}()" else "self.${cppNameCache.getName(field)}"
        return mapOf(
            "model" to field,
            "jsName" to nameRules.getName(field),
            "cppFullName" to cppNameCache.getFullyQualifiedName(struct),
            "cppType" to cppType,
            "cppFieldName" to if (hasAccessors) null else cppNameCache.getName(field),
            "hasAccessors" to hasAccessors,
            "hasBlob" to conversions.isBlob(field.typeRef),
            "isNullable" to field.typeRef.isNullable,
            "hasImmutableStruct" to conversions.isObjectStruct(field.typeRef),
            "hasDate" to conversions.isJsDate(field.typeRef),
            "hasLocale" to conversions.isJsLocale(field.typeRef),
            "hasDuration" to conversions.isJsDuration(field.typeRef),
            "cppGetterName" to cppNameCache.getGetterName(field),
            "cppSetterName" to cppNameCache.getSetterName(field),
            "accessorType" to accessorType,
            "hasCollection" to (field.typeRef.type.actualType is LimeList || field.typeRef.type.actualType is LimeMap || field.typeRef.type.actualType is LimeSet),
            "collectionGetter" to conversions.nativeToJs(field.typeRef, directSource),
            "collectionSetter" to convertedFieldSetter(field, hasAccessors),
            "immutableGetter" to conversions.nativeToJs(field.typeRef, directSource),
            "immutableSetter" to convertedFieldSetter(field, hasAccessors),
            "dateGetter" to conversions.nativeToJs(field.typeRef, directSource),
            "dateSetter" to convertedFieldSetter(field, hasAccessors),
            "localeGetter" to conversions.nativeToJs(field.typeRef, directSource),
            "localeSetter" to convertedFieldSetter(field, hasAccessors),
        )
    }

    private fun convertedFieldSetter(field: LimeField, hasAccessors: Boolean): String =
        conversions.jsToNative(field.typeRef, "value").let { converted -> if (hasAccessors) "self.${cppNameCache.getSetterName(field)}($converted)" else "self.${cppNameCache.getName(field)} = $converted" }

    fun propertyAdapterName(property: LimeProperty, operation: String) = "__gluecodium_${operation}_${property.fullName.replace(Regex("[^A-Za-z0-9_]"), "_")}"

    fun overloadRuntimeName(function: LimeFunction): String {
        val functionName = function.fullName.replace(Regex("[^A-Za-z0-9_]"), "_")
        val parameterTypes = function.parameters.joinToString("_") { embindNameResolver.resolveName(it.typeRef).replace(Regex("[^A-Za-z0-9_]"), "_") }
        return "__gluecodium_overload_${functionName}_${parameterTypes}"
    }

    fun structFunctionRuntimeName(function: LimeFunction): String =
        if (isJsOverloaded(function)) overloadRuntimeName(function) else "__gluecodium_struct_function_${function.fullName.replace(Regex("[^A-Za-z0-9_]"), "_")}"

    private fun isJsOverloaded(function: LimeFunction): Boolean {
        val container = referenceMap[function.path.parent.toString()] as? LimeContainer ?: return false
        val jsName = nameRules.getName(function)
        return container.functions.count { !it.isConstructor && nameRules.getName(it) == jsName } > 1
    }

    private fun isOverloadedInJsBindings(function: LimeFunction): Boolean {
        if (signatureResolver.isOverloadedInBindings(function)) return true
        val container = referenceMap[function.path.parent.toString()] as? LimeContainerWithInheritance ?: return false
        val functionName = nameRules.getName(function)
        return container.inheritedFunctions.any { !it.isStatic && nameRules.getName(it) == functionName }
    }

    fun overloadPredicate(function: LimeFunction): String {
        val checks = function.parameters.mapIndexed { index, parameter ->
            val value = "args[$index]"
            when (val actualType = parameter.typeRef.type.actualType) {
                is LimeBasicType -> when (actualType.typeId) {
                    LimeBasicType.TypeId.STRING -> "typeof $value === \"string\""
                    LimeBasicType.TypeId.BOOLEAN -> "typeof $value === \"boolean\""
                    LimeBasicType.TypeId.INT64, LimeBasicType.TypeId.UINT64, LimeBasicType.TypeId.DURATION -> "typeof $value === \"bigint\""
                    LimeBasicType.TypeId.DATE -> "$value instanceof Date"
                    LimeBasicType.TypeId.BLOB -> "$value instanceof Uint8Array"
                    else -> "typeof $value === \"number\""
                }
                is LimeList -> "Array.isArray($value)"
                is LimeMap -> "$value instanceof Map"
                is LimeSet -> "$value instanceof Set"
                is com.here.gluecodium.model.lime.LimeStruct -> structOverloadPredicate(value, actualType)
                else -> "$value !== null && typeof $value === \"object\""
            }
        }
        return listOf("args.length === ${function.parameters.size}", *checks.toTypedArray()).joinToString(" && ")
    }

    private fun structOverloadPredicate(value: String, struct: com.here.gluecodium.model.lime.LimeStruct): String {
        val fieldNames = struct.fields.map { nameRules.getName(it) }
        if (fieldNames.isEmpty()) return "$value !== null && typeof $value === \"object\""
        val names = fieldNames.joinToString(", ") { "\"${it.replace("\\", "\\\\").replace("\"", "\\\"")}\"" }
        return "$value !== null && typeof $value === \"object\" && Object.keys($value).every((key) => [$names].includes(key))"
    }

    private fun enumeratorViewModel(enumerator: com.here.gluecodium.model.lime.LimeEnumerator): Map<String, Any> =
        mapOf(
            "model" to enumerator,
            "jsName" to nameRules.getName(enumerator),
            "cppName" to "${cppNameCache.getFullyQualifiedName(getParentEnumeration(enumerator))}::${cppNameCache.getName(enumerator)}",
        )

    private fun getParentEnumeration(enumerator: com.here.gluecodium.model.lime.LimeEnumerator): LimeEnumeration =
        referenceMap[enumerator.path.parent.toString()] as? LimeEnumeration
            ?: throw IllegalStateException("Unable to resolve parent enumeration for ${enumerator.fullName}")

    private fun constantViewModel(constant: LimeConstant): Map<String, Any> =
        mapOf(
            "model" to constant,
            "jsName" to nameRules.getName(constant),
            "cppFullName" to cppNameCache.getFullyQualifiedName(constant),
            "cppType" to embindNameResolver.resolveName(constant.typeRef),
            "functionName" to "gluecodium_constant_${constant.fullName.replace('.', '_')}",
            "runtimeName" to "gluecodium_constant_${constant.fullName.replace(".", "__")}",
        )
}
