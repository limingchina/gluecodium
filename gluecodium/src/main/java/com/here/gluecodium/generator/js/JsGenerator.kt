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

import com.here.gluecodium.cli.GluecodiumExecutionException
import com.here.gluecodium.common.LimeLogger
import com.here.gluecodium.common.LimeModelFilter
import com.here.gluecodium.common.LimeModelSkipPredicates
import com.here.gluecodium.generator.common.GeneratedFile
import com.here.gluecodium.generator.common.Generator
import com.here.gluecodium.generator.common.GeneratorOptions
import com.here.gluecodium.generator.common.GenericImportsCollector
import com.here.gluecodium.generator.common.GenericIncludesCollector
import com.here.gluecodium.generator.common.Include
import com.here.gluecodium.generator.common.NameResolver
import com.here.gluecodium.generator.common.nameRuleSetFromConfig
import com.here.gluecodium.generator.cpp.CppNameCache
import com.here.gluecodium.generator.cpp.CppNameResolver
import com.here.gluecodium.generator.cpp.CppNameRules
import com.here.gluecodium.generator.cpp.CppSignatureResolver
import com.here.gluecodium.generator.common.templates.TemplateEngine
import com.here.gluecodium.model.lime.LimeAttributeType
import com.here.gluecodium.model.lime.LimeAttributeType.CPP
import com.here.gluecodium.model.lime.LimeAttributeType.JS
import com.here.gluecodium.model.lime.LimeAttributeValueType.ACCESSORS
import com.here.gluecodium.model.lime.LimeAttributeValueType.SKIP
import com.here.gluecodium.model.lime.LimeBasicType
import com.here.gluecodium.model.lime.LimeClass
import com.here.gluecodium.model.lime.LimeComment
import com.here.gluecodium.model.lime.LimeConstant
import com.here.gluecodium.model.lime.LimeContainerWithInheritance
import com.here.gluecodium.model.lime.LimeElement
import com.here.gluecodium.model.lime.LimeException
import com.here.gluecodium.model.lime.LimeExternalDescriptor
import com.here.gluecodium.model.lime.LimeField
import com.here.gluecodium.model.lime.LimeFieldConstructor
import com.here.gluecodium.model.lime.LimeFunction
import com.here.gluecodium.model.lime.LimeInterface
import com.here.gluecodium.model.lime.LimeLambda
import com.here.gluecodium.model.lime.LimeList
import com.here.gluecodium.model.lime.LimeMap
import com.here.gluecodium.model.lime.LimeModel
import com.here.gluecodium.model.lime.LimeNamedElement
import com.here.gluecodium.model.lime.LimeProperty
import com.here.gluecodium.model.lime.LimeSet
import com.here.gluecodium.model.lime.LimeStruct
import com.here.gluecodium.model.lime.LimeType
import com.here.gluecodium.model.lime.LimeTypeAlias
import com.here.gluecodium.model.lime.LimeTypeRef
import com.here.gluecodium.model.lime.LimeDirectTypeRef
import com.here.gluecodium.model.lime.LimeBasicType.TypeId
import java.util.logging.Logger

/**
 * Generates JavaScript/TypeScript bindings on top of the C++ API using Emscripten embind.
 *
 * <p>Architecturally this mirrors the Python generator: it produces TypeScript declaration stubs
 * (`.d.ts`) plus embind C++ binding files that `#include` the generated C++ headers and register
 * the C++ API via `EMSCRIPTEN_BINDINGS` blocks (no intermediate C-ABI shim). The entire output is
 * cross-compiled by `em++` into a single `.wasm` binary plus a JS glue/loader file.
 */
internal class JsGenerator : Generator {
    private lateinit var internalNamespace: List<String>
    private lateinit var rootNamespace: List<String>
    private lateinit var commentsProcessor: JsCommentsProcessor
    private lateinit var cppNameRules: CppNameRules
    private lateinit var nameRules: JsNameRules
    private lateinit var jsModuleName: String
    private lateinit var activeTags: Set<String>
    private var emitTypeScriptStubs = true

    private lateinit var limeReferenceMap: Map<String, LimeElement>
    private lateinit var jsNameResolver: JsNameResolver
    private lateinit var embindNameResolver: EmbindNameResolver
    private lateinit var cppNameCache: CppNameCache

    override val shortName = "js"

    override fun initialize(options: GeneratorOptions) {
        internalNamespace = options.cppInternalNamespace
        rootNamespace = options.cppRootNamespace
        commentsProcessor = JsCommentsProcessor(options.werror.contains(GeneratorOptions.WARNING_DOC_LINKS))
        cppNameRules = CppNameRules(rootNamespace, nameRuleSetFromConfig(options.cppNameRules))
        nameRules = JsNameRules(nameRuleSetFromConfig(options.jsNameRules))
        jsModuleName = options.jsModuleName
        activeTags = options.tags
        emitTypeScriptStubs = options.jsEmitTypeScriptStubs
    }

    override fun generate(limeModel: LimeModel): List<GeneratedFile> {
        val limeLogger = LimeLogger(logger, limeModel.fileNameMap)

        // Filter the model for the embind C++ binding output: retain functions/fields (needed
        // for binding bodies). External types are NOT skipped — embind still needs to `#include`
        // and bind external C++ types referenced by other bound types.
        val embindFilteredModel =
            LimeModelFilter.filter(limeModel) {
                LimeModelSkipPredicates.shouldRetainElement(it, activeTags, JS, retainFunctionsAndFields = true) &&
                    !isCppSkipped(it)
            }
        // Filter the model for the TypeScript `.d.ts` stub output.
        val jsFilteredModel =
            LimeModelFilter.filter(limeModel) {
                LimeModelSkipPredicates.shouldRetainElement(it, activeTags, JS, retainFunctionsAndFields = false)
            }

        jsNameResolver = JsNameResolver(embindFilteredModel.referenceMap, nameRules, limeLogger, commentsProcessor)

        limeReferenceMap = embindFilteredModel.referenceMap

        cppNameCache = CppNameCache(rootNamespace, embindFilteredModel.referenceMap, cppNameRules)
        embindNameResolver =
            EmbindNameResolver(
                embindFilteredModel.referenceMap,
                internalNamespace,
                cppNameCache,
                cppNameRules,
            )

        val nameResolvers =
            mapOf(
                "" to jsNameResolver,
                "Embind" to embindNameResolver,
                "C++" to embindNameResolver,
            )

        val importsCollector =
            GenericImportsCollector(
                JsImportResolver(limeReferenceMap, nameRules),
                collectTypeRefImports = true,
                collectValueImports = false,
                parentTypeFilter = { true },
                collectTypeAliasImports = true,
            )

        val stubFiles =
            if (emitTypeScriptStubs) {
                jsFilteredModel.topElements.flatMap { generateStubFile(it, importsCollector, nameResolvers) }
            } else {
                emptyList()
            }
        val embindFiles =
            embindFilteredModel.topElements.flatMap {
                generateEmbindFile(it, nameResolvers, embindFilteredModel)
            }

        if (commentsProcessor.hasError) {
            throw GluecodiumExecutionException("Validation errors found, see log for details.")
        }

        return stubFiles + embindFiles +
            generateCommonFiles(embindFilteredModel, jsFilteredModel, nameResolvers)
    }

    private fun generateStubFile(
        limeElement: LimeNamedElement,
        importsCollector: GenericImportsCollector<JsImport>,
        nameResolvers: Map<String, NameResolver>,
    ): List<GeneratedFile> {
        val templateName = selectStubTemplate(limeElement) ?: return emptyList()
        val selfModulePath = "./" + (limeElement.path.head + nameRules.getName(limeElement)).joinToString("/")
        val imports =
            importsCollector.collectImports(limeElement)
                .filterNot { it.modulePath == selfModulePath }
                .distinct()
                .sorted()

        val content =
            TemplateEngine.render(
                templateName,
                mapOf(
                    "model" to limeElement,
                    "imports" to imports,
                    "moduleName" to jsModuleName,
                ) + stubViewModel(limeElement),
                nameResolvers,
            )
        return listOf(GeneratedFile(content, nameRules.getJsStubFileName(limeElement)))
    }

    private fun stubViewModel(limeElement: LimeNamedElement): Map<String, Any> {
        val data = mutableMapOf<String, Any>(
            "jsName" to nameRules.getName(limeElement),
            "comment" to limeElement.comment,
            "additionalDescriptionComment" to LimeComment(),
            "hasDocumentation" to hasJsDocumentation(limeElement.comment),
        )
        val container = limeElement as? com.here.gluecodium.model.lime.LimeContainer
        if (container != null) {
            data["constructors"] = container.constructors.map { functionStubViewModel(it) }
            data["functions"] = container.functions.map { functionStubViewModel(it) }
            data["properties"] = container.properties.map {
                mapOf(
                    "jsName" to nameRules.getName(it),
                    "jsType" to jsNameResolver.resolveName(it.typeRef),
                    "isStatic" to it.isStatic,
                    "comment" to it.comment,
                    "additionalDescriptionComment" to it.additionalDescriptionComment,
                    "hasDocumentation" to
                        (hasJsDocumentation(it.comment) || hasJsDocumentation(it.additionalDescriptionComment)),
                )
            }
        }
        if (limeElement is LimeStruct) {
            data["fields"] = limeElement.fields.map {
                mapOf(
                    "jsName" to nameRules.getName(it),
                    "jsType" to jsNameResolver.resolveName(it.typeRef),
                    "comment" to it.comment,
                    "additionalDescriptionComment" to LimeComment(),
                    "hasDocumentation" to hasJsDocumentation(it.comment),
                )
            }
        }
        if (limeElement is com.here.gluecodium.model.lime.LimeEnumeration) {
            data["enumerators"] = limeElement.enumerators.map {
                mapOf(
                    "jsName" to nameRules.getName(it),
                    "comment" to it.comment,
                    "additionalDescriptionComment" to LimeComment(),
                    "hasDocumentation" to hasJsDocumentation(it.comment),
                )
            }
        }
        return data
    }

    private fun functionStubViewModel(function: LimeFunction): Map<String, Any> =
        mapOf(
            "jsName" to nameRules.getName(function),
            "comment" to function.comment,
            "hasDocumentation" to hasJsDocumentation(function),
            "isConstructor" to function.isConstructor,
            "isStatic" to function.isStatic,
            "returnType" to stubReturnType(function),
            "returnComment" to function.returnType.comment,
            "throwsComment" to (function.thrownType?.comment ?: LimeComment()),
            "parameters" to function.parameters.mapIndexed { index, parameter ->
                mapOf(
                    "jsName" to nameRules.getName(parameter),
                    "parameterName" to nameRules.getName(parameter),
                    "jsType" to jsNameResolver.resolveName(parameter.typeRef),
                    "comment" to parameter.comment,
                    "last" to (index == function.parameters.lastIndex),
                )
            },
        )

    private fun hasJsDocumentation(function: LimeFunction): Boolean =
        jsNameResolver.resolveName(function.comment).isNotBlank() ||
            function.parameters.any { jsNameResolver.resolveName(it.comment).isNotBlank() } ||
            jsNameResolver.resolveName(function.returnType.comment).isNotBlank() ||
            (function.thrownType?.comment?.let { jsNameResolver.resolveName(it).isNotBlank() } == true)

    private fun hasJsDocumentation(comment: LimeComment): Boolean =
        jsNameResolver.resolveName(comment).isNotBlank()

    private fun stubReturnType(function: LimeFunction): String {
        val exception = function.exception ?: return jsNameResolver.resolveName(function.returnType)
        val valueType = if (function.returnType.isVoid) null else jsNameResolver.resolveName(function.returnType)
        val errorType =
            if (exception.errorType.type.actualType is com.here.gluecodium.model.lime.LimeEnumeration) {
                "number"
            } else {
                jsNameResolver.resolveName(exception.errorType)
            }
        return listOfNotNull(valueType?.let { "value?: $it" }, "error?: $errorType")
            .joinToString("; ", prefix = "{ ", postfix = " }")
    }

    private fun generateEmbindFile(
        limeElement: LimeNamedElement,
        nameResolvers: Map<String, NameResolver>,
        filteredModel: LimeModel,
    ): List<GeneratedFile> {
        val limeType = limeElement as? com.here.gluecodium.model.lime.LimeType ?: return emptyList()
        val allTypes = collectEmbindTypes(limeType)
        if (allTypes.isEmpty()) return emptyList()

        val includeResolver = EmbindIncludeResolver(limeReferenceMap, cppNameRules, internalNamespace)
        val includeCollector = GenericIncludesCollector(includeResolver, retainPredicate = { true })
        val includes =
            allTypes.flatMap { includeCollector.collectImports(it) }.distinct().sorted()

        val bindings =
            allTypes.mapNotNull { type ->
                val templateName = selectEmbindTemplate(type) ?: return@mapNotNull null
                TemplateEngine.render(
                    templateName,
                    buildEmbindViewModel(type, filteredModel),
                    nameResolvers,
                )
            }

        val content =
            TemplateEngine.render(
                "js/EmbindFile",
                mapOf(
                    "includes" to includes,
                    "bindings" to bindings.joinToString("\n"),
                    "registerName" to resolveRegisterName(limeElement),
                ),
                nameResolvers,
            )
        return listOf(GeneratedFile(content, nameRules.getEmbindFileName(limeElement)))
    }

    /** Prefers an `open class` parent over a narrow interface as the single embind `base<>`. */
    private fun primaryBaseOf(
        type: com.here.gluecodium.model.lime.LimeType,
        filteredModel: LimeModel,
    ): String? =
        primaryBaseType(type, filteredModel)
            ?.let { cppNameCache.getFullyQualifiedName(it) }

    private fun primaryBaseType(
        type: com.here.gluecodium.model.lime.LimeType,
        filteredModel: LimeModel,
    ): LimeContainerWithInheritance? =
        (type as? LimeContainerWithInheritance)?.parents
            ?.mapNotNull { it.type.actualType as? LimeContainerWithInheritance }
            ?.filter { filteredModel.referenceMap.containsKey(it.fullName) }
            ?.minByOrNull { it is com.here.gluecodium.model.lime.LimeInterface }

    private fun secondaryParentMembers(
        type: com.here.gluecodium.model.lime.LimeType,
        filteredModel: LimeModel,
    ): Pair<List<LimeFunction>, List<LimeProperty>> {
        val container = type as? LimeContainerWithInheritance ?: return emptyList<LimeFunction>() to emptyList()
        val primaryBase = primaryBaseType(type, filteredModel)
        val secondaryParents =
            container.parents
                .mapNotNull { it.type.actualType as? LimeContainerWithInheritance }
                .filter { it !== primaryBase && filteredModel.referenceMap.containsKey(it.fullName) }
        val functions =
            secondaryParents
                .flatMap { it.functions + it.inheritedFunctions }
                .distinctBy { it.fullName }
        val properties =
            secondaryParents
                .flatMap { it.properties + it.inheritedProperties }
                .distinctBy { it.fullName }
        return functions to properties
    }

    /**
     * Builds the template data for one embind binding: the common identity fields plus
     * member view models (constructors, functions, properties, fields, enumerators,
     * constants) resolved against both the C++ names (for the binding body) and the JS
     * names (for the registered identifiers).
     */
    private fun buildEmbindViewModel(
        type: com.here.gluecodium.model.lime.LimeType,
        filteredModel: LimeModel,
    ): Map<String, Any> {
        val data = mutableMapOf<String, Any>(
            "model" to type,
            "internalNamespace" to internalNamespace,
            "jsName" to nameRules.getName(type),
            "embindName" to nameRules.getEmbindRuntimeName(type),
            "cppFullName" to cppNameCache.getFullyQualifiedName(type),
            "registerName" to resolveRegisterName(type),
            "isObjectStruct" to (type is LimeStruct && isObjectStruct(type)),
        )
        primaryBaseOf(type, filteredModel)?.let { data["primaryBase"] = it }
        if (type is com.here.gluecodium.model.lime.LimeEnumeration) {
            val enumerators = type.enumerators.map { enumeratorViewModel(it) }
            data["enumeratorBindings"] = enumerators.joinToString("\n") {
                "    .value(\"${it["jsName"]}\", ${it["cppName"]})"
            }
        }
        val container = type as? com.here.gluecodium.model.lime.LimeContainer ?: return data

        val (secondaryFunctions, secondaryProperties) = secondaryParentMembers(type, filteredModel)
        if (type is com.here.gluecodium.model.lime.LimeInterface) {
            val inheritedContainer = type as LimeContainerWithInheritance
            data["wrapperName"] = "${resolveRegisterName(type)}Wrapper"
            data["wrapperEmbindName"] = "${nameRules.getEmbindRuntimeName(type)}__Wrapper"
            data["wrapperPtrEmbindName"] = "${nameRules.getEmbindRuntimeName(type)}__WrapperPtr"
            data["wrapperMethods"] =
                (container.functions + inheritedContainer.inheritedFunctions)
                    .filterNot { it.isStatic || it.isConstructor }
                    .distinctBy { it.fullName }
                    .map { wrapperMethodViewModel(it) }
            data["wrapperProperties"] =
                (container.properties + inheritedContainer.inheritedProperties)
                    .distinctBy { it.fullName }
                    .map { wrapperPropertyViewModel(it) }
        }
        data["constructors"] = container.constructors.map { functionViewModel(it) }
        data["methods"] =
            (container.functions.filterNot { it.isConstructor } + secondaryFunctions)
                .distinctBy { it.fullName }
                .map {
                    functionViewModel(
                        it,
                        isFlattened = secondaryFunctions.contains(it),
                        flattenedReceiverType = cppNameCache.getFullyQualifiedName(type),
                        isPureVirtual = type is com.here.gluecodium.model.lime.LimeInterface,
                    )
                }
        data["properties"] =
            (container.properties + secondaryProperties)
                .distinctBy { it.fullName }
                .map { propertyViewModel(it) }
        if (type is LimeStruct) {
            data["fields"] = type.fields.map { fieldViewModel(type, it) }
        }
        data["constants"] = container.constants.filter(::isSupportedConstant).map { constantViewModel(it) }
        return data
    }

    private fun wrapperMethodViewModel(function: LimeFunction): Map<String, Any> {
        val returnType = embindNameResolver.resolveName(function.returnType)
        val parameters = function.parameters.map { parameter ->
            val nativeType = embindNameResolver.resolveName(parameter.typeRef)
            val parameterType =
                if (CppNameResolver.needsRefSuffix(parameter.typeRef)) "const $nativeType&" else nativeType
            "$parameterType ${parameter.path.name}"
        }
        val arguments = function.parameters.joinToString(", ") { it.path.name }
        val call = "call<$returnType>(\"${nameRules.getName(function)}\"${if (arguments.isNotEmpty()) ", $arguments" else ""})"
        return mapOf(
            "returnType" to returnType,
            "cppName" to embindNameResolver.resolveName(function),
            "parameters" to parameters.joinToString(", "),
            "call" to call,
            "isVoid" to function.returnType.isVoid,
        )
    }

    private fun wrapperPropertyViewModel(property: LimeProperty): Map<String, Any> {
        val propertyType = embindNameResolver.resolveName(property.typeRef)
        val setter = property.setter
        val setterParameter =
            if (CppNameResolver.needsRefSuffix(property.typeRef)) "const $propertyType& value" else "$propertyType value"
        return mapOf(
            "returnType" to propertyType,
            "jsName" to nameRules.getName(property),
            "cppGetterName" to cppNameCache.getGetterName(property),
            "cppSetterName" to cppNameCache.getSetterName(property),
            "setterParameter" to setterParameter,
            "hasSetter" to (setter != null),
        )
    }

    private fun functionViewModel(
        function: LimeFunction,
        isFlattened: Boolean = false,
        flattenedReceiverType: String? = null,
        isPureVirtual: Boolean = false,
    ): Map<String, Any> {
        val isOverloaded = CppSignatureResolver(limeReferenceMap, cppNameRules).isOverloaded(function)
        val embindName =
            if (isOverloaded && function.isStatic && isJsOverloaded(function)) {
                overloadRuntimeName(function)
            } else {
                nameRules.getName(function)
            }
        val returnType = function.returnType.typeRef
        val returnActualType = returnType.type.actualType
        val thrownException = function.exception
        val thrownErrorIsEnum =
            thrownException?.errorType?.type?.actualType is com.here.gluecodium.model.lime.LimeEnumeration
        val needsAdapter =
            isOverloaded ||
            thrownException != null ||
                returnType.isNullable ||
                isJsDate(returnType) ||
                isJsLocale(returnType) ||
                isJsDuration(returnType) ||
                returnActualType is LimeList ||
                returnActualType is LimeMap ||
                returnActualType is LimeSet ||
                isBlob(returnType) ||
                isObjectStruct(returnType) ||
                function.parameters.any { parameter ->
                    parameter.typeRef.isNullable ||
                        parameter.typeRef.type.actualType is LimeList ||
                        parameter.typeRef.type.actualType is LimeMap ||
                        parameter.typeRef.type.actualType is LimeSet ||
                    isBlob(parameter.typeRef) ||
                        isObjectStruct(parameter.typeRef) ||
                        parameter.typeRef.type.actualType is LimeLambda ||
                        isJsDate(parameter.typeRef) ||
                        isJsLocale(parameter.typeRef) ||
                        isJsDuration(parameter.typeRef) ||
                        hasCppStringOverride(parameter.typeRef)
                }
        return mapOf(
            "model" to function,
            "jsName" to nameRules.getName(function),
            "embindName" to embindName,
            "cppName" to embindNameResolver.resolveName(function),
            "isConstructor" to function.isConstructor,
            "isStatic" to function.isStatic,
            "needsAdapter" to needsAdapter,
            "adapterReturnType" to
                if (
                    thrownException != null ||
                        returnType.isNullable ||
                        isJsDate(returnType) ||
                        isJsLocale(returnType) ||
                        isJsDuration(returnType) ||
                        returnActualType is LimeList ||
                        returnActualType is LimeMap ||
                        returnActualType is LimeSet ||
                        isBlob(returnType) ||
                        isObjectStruct(returnType)
                ) {
                    "emscripten::val"
                } else {
                    embindNameResolver.resolveName(returnType)
                },
            "isThrown" to (thrownException != null),
            "thrownErrorIsEnum" to thrownErrorIsEnum,
            "returnIsNullable" to returnType.isNullable,
            "returnIsList" to (returnActualType is LimeList),
            "returnIsMap" to (returnActualType is LimeMap),
            // Overloads are registered with explicit signatures via select_overload.
            "isOverloaded" to isOverloaded,
            "isFlattened" to isFlattened,
            "isPureVirtual" to isPureVirtual,
            "parameters" to function.parameters.mapIndexed { index, parameter ->
                val actualType = parameter.typeRef.type.actualType
                mapOf(
                    "model" to parameter,
                    "jsName" to nameRules.getName(parameter),
                    "cppType" to embindNameResolver.resolveName(parameter.typeRef),
                    "adapterType" to
                        if (hasCppStringOverride(parameter.typeRef)) {
                            "::std::string"
                        } else if (
                            parameter.typeRef.isNullable ||
                            isJsDate(parameter.typeRef) ||
                            isJsLocale(parameter.typeRef) ||
                            isJsDuration(parameter.typeRef) ||
                                actualType is LimeList ||
                                actualType is LimeMap ||
                                actualType is LimeSet ||
                                isBlob(parameter.typeRef) ||
                                isObjectStruct(parameter.typeRef) ||
                                actualType is LimeLambda
                        ) {
                            "emscripten::val"
                        } else {
                            embindNameResolver.resolveName(parameter.typeRef)
                        },
                    "nativeName" to parameter.path.name,
                    "nativeType" to embindNameResolver.resolveName(parameter.typeRef),
                    "underlyingType" to embindNameResolver.resolveName(parameter.typeRef.type),
                    "isNullable" to parameter.typeRef.isNullable,
                    "isList" to (actualType is LimeList),
                    "isMap" to (actualType is LimeMap),
                    "mapKeyType" to (actualType as? LimeMap)?.let { embindNameResolver.resolveName(it.keyType) },
                    "mapValueType" to (actualType as? LimeMap)?.let { embindNameResolver.resolveName(it.valueType) },
                    "last" to (index == function.parameters.lastIndex),
                )
            },
        ).toMutableMap().apply {
            val parameters = function.parameters.mapIndexed { index, parameter ->
                val actualType = parameter.typeRef.type.actualType
                val nativeType = embindNameResolver.resolveName(parameter.typeRef)
                val adapterType =
                    if (hasCppStringOverride(parameter.typeRef)) {
                        "::std::string"
                    } else if (
                        parameter.typeRef.isNullable ||
                        isJsDate(parameter.typeRef) ||
                        isJsLocale(parameter.typeRef) ||
                        isJsDuration(parameter.typeRef) ||
                            actualType is LimeList ||
                            actualType is LimeMap ||
                            actualType is LimeSet ||
                            isBlob(parameter.typeRef) ||
                            isObjectStruct(parameter.typeRef) ||
                            actualType is LimeLambda
                    ) {
                        "emscripten::val"
                    } else {
                        nativeType
                    }
                val callName = if (hasCppStringOverride(parameter.typeRef)) {
                    "${parameter.path.name}.c_str()"
                } else if (
                        parameter.typeRef.isNullable ||
                        isJsDate(parameter.typeRef) ||
                        isJsLocale(parameter.typeRef) ||
                    isJsDuration(parameter.typeRef) ||
                        actualType is LimeList ||
                        actualType is LimeMap ||
                        actualType is LimeSet ||
                        isBlob(parameter.typeRef) ||
                        isObjectStruct(parameter.typeRef) ||
                        actualType is LimeLambda
                ) {
                    "${parameter.path.name}_value"
                } else {
                    parameter.path.name
                }
                mapOf(
                    "type" to adapterType,
                    "name" to parameter.path.name,
                    "last" to (index == function.parameters.lastIndex),
                    "callName" to callName,
                    "preparation" to adapterParameterPreparation(parameter, callName),
                )
            }
            put("adapterParameters", parameters.joinToString(", ") { "${it["type"]} ${it["name"]}" })
            put("adapterSignatureParameters", parameters.joinToString(", ") { it["type"].toString() })
            put("adapterCallArguments", parameters.joinToString(", ") { it["callName"].toString() })
            put(
                "adapterPolicies",
                parameters.mapIndexedNotNull { index, parameter ->
                    if (parameter["type"].toString().endsWith("*")) {
                        "allow_raw_pointer<arg<$index>>()"
                    } else {
                        null
                    }
                }.joinToString(", "),
            )
            put("hasAdapterPolicies", parameters.any { it["type"].toString().endsWith("*") })
            put(
                "adapterMemberPolicies",
                parameters.mapIndexedNotNull { index, parameter ->
                    if (parameter["type"].toString().endsWith("*")) {
                        "allow_raw_pointer<arg<${index + 1}>>()"
                    } else {
                        null
                    }
                }.joinToString(", "),
            )
            put("hasAdapterMemberPolicies", parameters.any { it["type"].toString().endsWith("*") })
            put("adapterPreparations", parameters.map { it["preparation"] }.filter { it is String && it.isNotEmpty() }.joinToString("\n"))
            put(
                "adapterCallPrefix",
                if (returnType.isNullable || isJsDate(returnType) || isJsLocale(returnType) || isJsDuration(returnType) || returnActualType is LimeList || returnActualType is LimeMap || returnActualType is LimeSet || isBlob(returnType) || isObjectStruct(returnType)) {
                    "auto result = "
                } else if (thrownException != null) {
                    "auto result = "
                } else {
                    "return "
                },
            )
            put("adapterReturnConversion", if (thrownException != null) {
                thrownReturnConversion(thrownErrorIsEnum, function.returnType.isVoid, returnType)
            } else {
                adapterReturnConversion(returnType, returnActualType)
            })
            if (isFlattened) {
                val receiverType = flattenedReceiverType ?: error("Missing flattened receiver type")
                val flattenedReturnType =
                    if (
                        thrownException != null ||
                            returnType.isNullable ||
                            isJsDate(returnType) ||
                            isJsLocale(returnType) ||
                            isJsDuration(returnType) ||
                            returnActualType is LimeList ||
                            returnActualType is LimeMap ||
                            returnActualType is LimeSet ||
                            isBlob(returnType) ||
                            isObjectStruct(returnType)
                    ) {
                        "emscripten::val"
                    } else {
                        embindNameResolver.resolveName(returnType)
                    }
                put(
                    "flattenedFunctionSignature",
                    listOf(
                        "$flattenedReturnType($receiverType*",
                        *parameters.map { it["type"].toString() }.toTypedArray(),
                    )
                        .joinToString(", ")
                        .let { "$it)" },
                )
                put(
                    "flattenedLambdaParameters",
                    listOf("$receiverType* self", *parameters.map { "${it["type"]} ${it["name"]}" }.toTypedArray())
                        .joinToString(", "),
                )
            }
        }
    }

    private fun adapterParameterPreparation(parameter: com.here.gluecodium.model.lime.LimeParameter, callName: String): String {
        val typeRef = parameter.typeRef
        val actualType = typeRef.type.actualType
        return when {
            actualType is LimeLambda -> lambdaAdapterPreparation(actualType, parameter.path.name, callName)
            typeRef.isNullable || isJsDate(typeRef) || isJsLocale(typeRef) || isJsDuration(typeRef) || actualType is LimeList || actualType is LimeMap || actualType is LimeSet || isBlob(typeRef) || isObjectStruct(typeRef) ->
                "auto $callName = ${jsToNative(typeRef, parameter.path.name)};"
            else -> ""
        }
    }

    private fun hasCppStringOverride(typeRef: LimeTypeRef): Boolean {
        val actualType = typeRef.type.actualType
        return actualType is LimeBasicType &&
            actualType.typeId == TypeId.STRING &&
            typeRef.attributes.get(com.here.gluecodium.model.lime.LimeAttributeType.CPP, com.here.gluecodium.model.lime.LimeAttributeValueType.TYPE) != null
    }

    private fun isBlob(typeRef: LimeTypeRef): Boolean =
        (typeRef.type.actualType as? LimeBasicType)?.typeId == TypeId.BLOB

    private fun isObjectStruct(typeRef: LimeTypeRef): Boolean =
        (typeRef.type.actualType as? LimeStruct)?.let(::isObjectStruct) == true

    private fun isObjectStruct(struct: LimeStruct): Boolean =
        struct.attributes.have(LimeAttributeType.IMMUTABLE) ||
            struct.fields.any { isObjectStruct(it.typeRef) }

    private fun isJsDate(typeRef: LimeTypeRef): Boolean =
        (typeRef.type.actualType as? LimeBasicType)?.typeId == TypeId.DATE &&
            !hasCppTypeOverride(typeRef)

    private fun isJsDuration(typeRef: LimeTypeRef): Boolean =
        (typeRef.type.actualType as? LimeBasicType)?.typeId == TypeId.DURATION

    private fun isJsLocale(typeRef: LimeTypeRef): Boolean =
        (typeRef.type.actualType as? LimeBasicType)?.typeId == TypeId.LOCALE

    private fun hasCppTypeOverride(typeRef: LimeTypeRef): Boolean {
        if (typeRef.attributes.have(CPP, com.here.gluecodium.model.lime.LimeAttributeValueType.TYPE)) return true
        val alias = typeRef.type as? LimeTypeAlias ?: return false
        return hasCppTypeOverride(alias.typeRef)
    }

    private fun requiresJsAdapter(typeRef: LimeTypeRef): Boolean {
        if (typeRef.isNullable || isJsDate(typeRef) || isJsLocale(typeRef) || isJsDuration(typeRef) || isBlob(typeRef) || isObjectStruct(typeRef)) return true
        return when (val actualType = typeRef.type.actualType) {
            is LimeList -> requiresJsAdapter(actualType.elementType)
            is LimeMap -> requiresJsAdapter(actualType.keyType) || requiresJsAdapter(actualType.valueType)
            is LimeSet -> requiresJsAdapter(actualType.elementType)
            is LimeLambda -> true
            else -> false
        }
    }

    private fun jsToNative(typeRef: LimeTypeRef, source: String): String {
        if (typeRef.isNullable) {
            val nativeType = embindNameResolver.resolveName(typeRef)
            val value = jsToNativeNonNullable(typeRef.type.actualType, typeRef, source)
            return "($source.isNull() || $source.isUndefined() ? " +
                "$nativeType{} : $nativeType($value))"
        }
        return jsToNativeNonNullable(typeRef.type.actualType, typeRef, source)
    }

    private fun jsToNativeNonNullable(actualType: LimeType, typeRef: LimeTypeRef, source: String): String =
        when (actualType) {
            is LimeList -> {
                val element = jsToNative(actualType.elementType, "entry")
                "([&]() { ${embindNameResolver.resolveName(typeRef.type)} converted; " +
                    "for (const auto& entry : $source.call<emscripten::val>(\"values\")) { " +
                    "converted.emplace_back($element); } return converted; }())"
            }
            is LimeMap -> {
                val key = jsToNative(actualType.keyType, "entry[0]")
                val value = jsToNative(actualType.valueType, "entry[1]")
                "([&]() { ${embindNameResolver.resolveName(typeRef.type)} converted; " +
                    "for (const auto& entry : $source.call<emscripten::val>(\"entries\")) { " +
                    "converted.emplace($key, $value); } return converted; }())"
            }
            is LimeSet -> {
                val element = jsToNative(actualType.elementType, "entry")
                "([&]() { ${embindNameResolver.resolveName(typeRef.type)} converted; " +
                    "for (const auto& entry : $source.call<emscripten::val>(\"values\")) { " +
                    "converted.emplace($element); } return converted; }())"
            }
            is LimeStruct -> if (isObjectStruct(actualType)) {
                val arguments = actualType.fields.joinToString(", ") { field ->
                    jsToNative(field.typeRef, "$source[\"${nameRules.getName(field)}\"]")
                }
                "${cppNameCache.getFullyQualifiedName(actualType)}($arguments)"
            } else {
                "$source.as<${embindNameResolver.resolveName(typeRef)}>()"
            }
            is LimeBasicType ->
                if (actualType.typeId == TypeId.DATE && isJsDate(typeRef)) {
                    "gluecodium_date_to_native<${embindNameResolver.resolveName(typeRef.type)}>( $source )"
                } else if (actualType.typeId == TypeId.LOCALE) {
                    "gluecodium_locale_to_native($source)"
                } else if (actualType.typeId == TypeId.DURATION) {
                    val nativeTypeRef = LimeDirectTypeRef(typeRef.type, false, typeRef.attributes)
                    "gluecodium_duration_to_native<${embindNameResolver.resolveName(nativeTypeRef)}>( $source )"
                } else if (actualType.typeId == TypeId.BLOB) {
                    "::std::make_shared<::std::vector<uint8_t>>(emscripten::convertJSArrayToNumberVector<uint8_t>($source))"
                } else {
                    "$source.as<${embindNameResolver.resolveName(typeRef)}>()"
                }
            else -> "$source.as<${embindNameResolver.resolveName(typeRef)}>()"
        }

    private fun lambdaAdapterPreparation(lambda: LimeLambda, parameterName: String, callName: String): String {
        val function = lambda.asFunction()
        val returnType = embindNameResolver.resolveName(function.returnType)
        val parameters = function.parameters.map { parameter ->
            val type = embindNameResolver.resolveName(parameter.typeRef)
            val cppType = if (CppNameResolver.needsRefSuffix(parameter.typeRef)) "const $type&" else type
            "$cppType ${parameter.path.name}"
        }
        val arguments = function.parameters.joinToString(", ") { it.path.name }
        val invocation = "${parameterName}.call<$returnType>(\"call\", $parameterName${if (arguments.isNotEmpty()) ", $arguments" else ""})"
        val body = if (function.returnType.isVoid) "$invocation;" else "return $invocation;"
        return "auto $callName = [$parameterName = std::move($parameterName)](${parameters.joinToString(", ")}) -> $returnType { $body };"
    }

    private fun adapterReturnConversion(
        returnType: com.here.gluecodium.model.lime.LimeTypeRef,
        actualType: com.here.gluecodium.model.lime.LimeType,
    ): String {
        return if (returnType.isNullable || isJsDate(returnType) || isJsLocale(returnType) || isJsDuration(returnType) || actualType is LimeList || actualType is LimeMap || actualType is LimeSet || isBlob(returnType) || isObjectStruct(returnType)) {
            "return ${nativeToJs(returnType, "result")};"
        } else {
            ""
        }
    }

    private fun nativeToJs(typeRef: LimeTypeRef, source: String): String {
        if (typeRef.isNullable) {
            return "($source ? ${nativeToJsNonNullable(typeRef.type.actualType, typeRef, "*$source")} : emscripten::val::undefined())"
        }
        return nativeToJsNonNullable(typeRef.type.actualType, typeRef, source)
    }

    private fun nativeToJsNonNullable(actualType: LimeType, typeRef: LimeTypeRef, source: String): String =
        when (actualType) {
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
                    val fieldSource = if (actualType.attributes.have(CPP, ACCESSORS)) {
                        "$source.${cppNameCache.getGetterName(field)}()"
                    } else {
                        "$source.${cppNameCache.getName(field)}"
                    }
                    "jsResult.set(\"${nameRules.getName(field)}\", ${nativeToJs(field.typeRef, fieldSource)});"
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
                    "($source ? emscripten::val::array(*$source) : emscripten::val::array(::std::vector<uint8_t>{}))"
                } else {
                    "emscripten::val($source)"
                }
            else -> "emscripten::val($source)"
        }

    private fun thrownReturnConversion(errorIsEnum: Boolean, returnIsVoid: Boolean, returnType: LimeTypeRef): String {
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

    private fun propertyViewModel(property: LimeProperty): Map<String, Any> =
        mapOf(
            "model" to property,
            "jsName" to nameRules.getName(property),
            "cppGetterName" to cppNameCache.getGetterName(property),
            "cppSetterName" to cppNameCache.getSetterName(property),
            "isStatic" to property.isStatic,
            "hasSetter" to (property.setter != null),
            "cppFullName" to ((limeReferenceMap[property.path.parent.toString()] as? LimeNamedElement)
                ?.let { cppNameCache.getFullyQualifiedName(it) } ?: ""),
            "needsAdapter" to requiresJsAdapter(property.typeRef),
            "adapterGetterName" to propertyAdapterName(property, "get"),
            "adapterSetterName" to propertyAdapterName(property, "set"),
            "adapterGetter" to nativeToJs(
                property.typeRef,
                if (property.isStatic) {
                    "${cppNameCache.getFullyQualifiedName(limeReferenceMap[property.path.parent.toString()] as LimeNamedElement)}::${cppNameCache.getGetterName(property)}()"
                } else {
                    "self->${cppNameCache.getGetterName(property)}()"
                },
            ),
            "adapterSetter" to jsToNative(property.typeRef, "value").let { converted ->
                if (property.isStatic) {
                    "${cppNameCache.getFullyQualifiedName(limeReferenceMap[property.path.parent.toString()] as LimeNamedElement)}::${cppNameCache.getSetterName(property)}($converted)"
                } else {
                    "self->${cppNameCache.getSetterName(property)}($converted)"
                }
            },
        )

    private fun fieldViewModel(struct: LimeStruct, field: LimeField): Map<String, Any?> =
        run {
            val cppType = embindNameResolver.resolveName(field.typeRef)
            val hasAccessors =
                struct.attributes.have(CPP, ACCESSORS) ||
                    field.external?.cpp?.get(LimeExternalDescriptor.Companion.GETTER_NAME_NAME) != null
            val accessorType = if (CppNameResolver.needsRefSuffix(field.typeRef)) "const $cppType&" else cppType
            mapOf(
                "model" to field,
                "jsName" to nameRules.getName(field),
                "cppFullName" to cppNameCache.getFullyQualifiedName(struct),
                "cppType" to cppType,
                "cppFieldName" to if (hasAccessors) null else cppNameCache.getName(field),
                "hasAccessors" to hasAccessors,
                "hasBlob" to isBlob(field.typeRef),
                "hasImmutableStruct" to isObjectStruct(field.typeRef),
            "hasDate" to isJsDate(field.typeRef),
            "hasLocale" to isJsLocale(field.typeRef),
            "hasDuration" to isJsDuration(field.typeRef),
                "cppGetterName" to cppNameCache.getGetterName(field),
                "cppSetterName" to cppNameCache.getSetterName(field),
                "accessorType" to accessorType,
                "hasCollection" to (!hasAccessors &&
                    (field.typeRef.type.actualType is LimeList ||
                    field.typeRef.type.actualType is LimeMap ||
                    field.typeRef.type.actualType is LimeSet)),
                "collectionGetter" to nativeToJs(field.typeRef, "self.${cppNameCache.getName(field)}"),
                "collectionSetter" to jsToNative(field.typeRef, "value"),
                "immutableGetter" to nativeToJs(
                    field.typeRef,
                    if (hasAccessors) "self.${cppNameCache.getGetterName(field)}()" else "self.${cppNameCache.getName(field)}",
                ),
                "immutableSetter" to jsToNative(field.typeRef, "value").let { converted ->
                    if (hasAccessors) {
                        "self.${cppNameCache.getSetterName(field)}($converted)"
                    } else {
                        "self.${cppNameCache.getName(field)} = $converted"
                    }
                },
                "dateGetter" to nativeToJs(field.typeRef, if (hasAccessors) {
                    "self.${cppGetterName(field)}()"
                } else {
                    "self.${cppNameCache.getName(field)}"
                }),
                "dateSetter" to jsToNative(field.typeRef, "value").let { converted -> if (hasAccessors) {
                    "self.${cppSetterName(field)}($converted)"
                } else {
                    "self.${cppNameCache.getName(field)} = $converted"
                } },
                "localeGetter" to nativeToJs(field.typeRef, if (hasAccessors) {
                    "self.${cppGetterName(field)}()"
                } else {
                    "self.${cppNameCache.getName(field)}"
                }),
                "localeSetter" to jsToNative(field.typeRef, "value").let { converted -> if (hasAccessors) {
                    "self.${cppSetterName(field)}($converted)"
                } else {
                    "self.${cppNameCache.getName(field)} = $converted"
                } },
            )
        }

    private fun cppGetterName(field: LimeField) = cppNameCache.getGetterName(field)

    private fun cppSetterName(field: LimeField) = cppNameCache.getSetterName(field)

    private fun propertyAdapterName(property: LimeProperty, operation: String) =
        "__gluecodium_${operation}_${property.fullName.replace(Regex("[^A-Za-z0-9_]"), "_")}"

    private fun overloadRuntimeName(function: LimeFunction): String {
        val functionName = function.fullName.replace(Regex("[^A-Za-z0-9_]"), "_")
        val parameterTypes = function.parameters.joinToString("_") {
            embindNameResolver.resolveName(it.typeRef).replace(Regex("[^A-Za-z0-9_]"), "_")
        }
        return "__gluecodium_overload_${functionName}_${parameterTypes}"
    }

    private fun isJsOverloaded(function: LimeFunction): Boolean {
        val container = limeReferenceMap[function.path.parent.toString()] as? com.here.gluecodium.model.lime.LimeContainer
            ?: return false
        val jsName = nameRules.getName(function)
        return container.functions.count { !it.isConstructor && nameRules.getName(it) == jsName } > 1
    }

    private fun overloadPredicate(function: LimeFunction): String {
        val checks = function.parameters.mapIndexed { index, parameter ->
            val value = "args[$index]"
            val actualType = parameter.typeRef.type.actualType
            when (actualType) {
                is LimeBasicType -> when (actualType.typeId) {
                    TypeId.STRING -> "typeof $value === \"string\""
                    TypeId.BOOLEAN -> "typeof $value === \"boolean\""
                    TypeId.INT64, TypeId.UINT64, TypeId.DURATION -> "typeof $value === \"bigint\""
                    TypeId.DATE -> "$value instanceof Date"
                    TypeId.BLOB -> "$value instanceof Uint8Array"
                    else -> "typeof $value === \"number\""
                }
                is LimeList -> "Array.isArray($value)"
                is LimeMap -> "$value instanceof Map"
                is LimeSet -> "$value instanceof Set"
                else -> "$value !== null && typeof $value === \"object\""
            }
        }
        return listOf("args.length === ${function.parameters.size}", *checks.toTypedArray()).joinToString(" && ")
    }

    private fun enumeratorViewModel(enumerator: com.here.gluecodium.model.lime.LimeEnumerator): Map<String, Any> =
        mapOf(
            "model" to enumerator,
            "jsName" to nameRules.getName(enumerator),
            "cppName" to
                "${cppNameCache.getFullyQualifiedName(getParentEnumeration(enumerator))}::${cppNameCache.getName(enumerator)}",
        )

    private fun getParentEnumeration(enumerator: com.here.gluecodium.model.lime.LimeEnumerator): com.here.gluecodium.model.lime.LimeEnumeration =
        limeReferenceMap[enumerator.path.parent.toString()] as? com.here.gluecodium.model.lime.LimeEnumeration
            ?: throw IllegalStateException("Unable to resolve parent enumeration for ${enumerator.fullName}")

    private fun constantViewModel(constant: LimeConstant): Map<String, Any> =
        mapOf(
            "model" to constant,
            "jsName" to nameRules.getName(constant),
            "cppFullName" to cppNameCache.getFullyQualifiedName(constant),
            "cppType" to embindNameResolver.resolveName(constant.typeRef),
            "functionName" to constantFunctionName(constant),
            "runtimeName" to constantRuntimeName(constant),
        )

    private fun constantFunctionName(constant: LimeConstant) =
        "gluecodium_constant_${constant.fullName.replace('.', '_')}"

    private fun constantRuntimeName(constant: LimeConstant) =
        "gluecodium_constant_${constant.fullName.replace(".", "__")}"

    /**
     * Recursively collects all types (top-level + nested) that should emit an embind binding,
     * in parent-before-child order. Excludes type aliases and lambdas (which emit no binding).
     */
    private fun collectEmbindTypes(limeType: com.here.gluecodium.model.lime.LimeType): List<com.here.gluecodium.model.lime.LimeType> {
        val result = mutableListOf<com.here.gluecodium.model.lime.LimeType>()
        if (limeType !is com.here.gluecodium.model.lime.LimeTypeAlias && limeType !is LimeLambda) {
            result.add(limeType)
        }
        val container = limeType as? com.here.gluecodium.model.lime.LimeContainer ?: return result
        val nestedTypes =
            container.structs + container.classes + container.interfaces +
                container.enumerations + container.exceptions +
                container.typeAliases + container.lambdas
        for (nested in nestedTypes) {
            result.addAll(collectEmbindTypes(nested))
        }
        return result
    }

    private fun generateCommonFiles(
        filteredModel: LimeModel,
        jsFilteredModel: LimeModel,
        nameResolvers: Map<String, NameResolver>,
    ): List<GeneratedFile> {
        // Module init: aggregates every per-top-level-element register_* call inside one
        // EMSCRIPTEN_BINDINGS block, in dependency order (bases before derived types).
        val topLevelBoundTypes =
            filteredModel.topElements
                .filterIsInstance<com.here.gluecodium.model.lime.LimeType>()
                .filter { it !is com.here.gluecodium.model.lime.LimeTypeAlias && it !is LimeLambda }
        val boundTypes = topLevelBoundTypes.flatMap(::collectEmbindTypes)
        val boundTypeNames = boundTypes.map(::resolveRegisterName).toSet()
        val registerNameToDeps =
            boundTypes.associate { type ->
                val registerName = resolveRegisterName(type)
                val nestedTypeDeps =
                    if (type in topLevelBoundTypes) {
                        collectEmbindTypes(type).drop(1).map(::resolveRegisterName)
                    } else {
                        emptyList()
                    }
                val parentDeps =
                    (type as? LimeContainerWithInheritance)?.parents
                        ?.mapNotNull { it.type.actualType as? LimeNamedElement }
                        ?.map(::resolveRegisterName)
                        .orEmpty()
                registerName to (nestedTypeDeps + parentDeps)
                    .filter { it != registerName && it in boundTypeNames }
                    .distinct()
            }
        val genericRegistrations = collectGenericRegistrations(filteredModel)
        val genericRegistrationIncludes = collectGenericRegistrationIncludes(filteredModel)
        val moduleInitContent =
            TemplateEngine.render(
                "js/EmbindModuleInit",
                mapOf(
                    "moduleName" to jsModuleName,
                    "registerFunctions" to topologicalSort(registerNameToDeps).map { mapOf("name" to it) },
                    "genericRegistrations" to genericRegistrations,
                    "genericRegistrationIncludes" to genericRegistrationIncludes,
                    "needsUnorderedSet" to containsNullableSet(filteredModel),
                    "localeTypeName" to embindNameResolver.resolveName(TypeId.LOCALE),
                    "localeInclude" to (internalNamespace + "Locale.h").joinToString("/"),
                ),
                nameResolvers,
            )
        val wrapperTypeNames =
            filteredModel.topElements
                .filterIsInstance<com.here.gluecodium.model.lime.LimeType>()
                .flatMap(::collectEmbindTypes)
                .filter { it is LimeClass || it is LimeInterface }
                .map { nameRules.getEmbindRuntimeName(it) }
                .distinct()
        val wrapperTypes =
            wrapperTypeNames.mapIndexed { index, name ->
                mapOf("name" to name, "last" to (index == wrapperTypeNames.lastIndex))
            }
        val wrapperRuntimeContent =
            TemplateEngine.render(
                "js/JsWrapperRuntime",
                mapOf("wrapperTypes" to wrapperTypes),
                nameResolvers,
            )
        val moduleRuntimeContent =
            TemplateEngine.render(
                "js/JsModuleRuntime",
                mapOf("moduleFileName" to jsModuleName),
                nameResolvers,
            )
        val packageFiles = generatePackageFiles(jsFilteredModel, nameResolvers)
        return packageFiles + listOf(
            GeneratedFile(moduleInitContent, JsNameRules.MODULE_INIT_FILE),
            GeneratedFile(wrapperRuntimeContent, JsNameRules.WRAPPER_RUNTIME_FILE),
            GeneratedFile(moduleRuntimeContent, JsNameRules.MODULE_RUNTIME_FILE),
        )
    }

    private fun generatePackageFiles(
        filteredModel: LimeModel,
        nameResolvers: Map<String, NameResolver>,
    ): List<GeneratedFile> {
        val packageTypes =
            filteredModel.topElements
                .filterIsInstance<LimeNamedElement>()
                .groupBy { it.path.head }
                .toSortedMap(compareBy { it.joinToString(".") })
        val indexFiles =
            packageTypes.map { (packagePath, elements) ->
                val exports =
                    elements
                        .sortedBy { nameRules.getName(it) }
                        .map { mapOf("moduleName" to nameRules.getName(it)) }
                val content =
                    TemplateEngine.render(
                        "js/JsIndex",
                        mapOf("exports" to exports),
                        nameResolvers,
                    )
                val directory = packagePath.joinToString(java.io.File.separator)
                val runtimeElements =
                    elements
                        .filterIsInstance<com.here.gluecodium.model.lime.LimeType>()
                        .flatMap(::collectEmbindTypes)
                        .filter { it is com.here.gluecodium.model.lime.LimeClass ||
                            it is com.here.gluecodium.model.lime.LimeInterface ||
                            it is LimeStruct ||
                            it is com.here.gluecodium.model.lime.LimeEnumeration }
                        .distinctBy { it.fullName }
                        .sortedWith(compareBy({ nameRules.getName(it) }, { it.fullName }))
                val preferredNameCounts =
                    runtimeElements
                        .filter { it.path.hasParent }
                        .groupingBy { nameRules.getName(it) }
                        .eachCount()
                val runtimeExports =
                    runtimeElements
                        .map { element ->
                            val preferredName = nameRules.getName(element)
                            val isNested = element.path.hasParent
                            val moduleName =
                                if (isNested &&
                                    (preferredNameCounts[preferredName] ?: 0) > 1
                                ) {
                                    nameRules.getFlattenedName(element)
                                } else {
                                    preferredName
                                }
                            mapOf(
                                "moduleName" to moduleName,
                                "runtimeName" to nameRules.getEmbindRuntimeName(element),
                                "isStruct" to (element is LimeStruct),
                                "constants" to (element as? com.here.gluecodium.model.lime.LimeContainer)
                                    ?.constants
                                    ?.filter(::isSupportedConstant)
                                    ?.filterNot(::isCppSkipped)
                                    ?.map { constant ->
                                        mapOf(
                                            "jsName" to nameRules.getName(constant),
                                            "runtimeName" to constantRuntimeName(constant),
                                        )
                                    }
                                    .orEmpty(),
                                "properties" to (element as? com.here.gluecodium.model.lime.LimeContainer)
                                    ?.properties
                                    ?.filter { it.isStatic && requiresJsAdapter(it.typeRef) }
                                    ?.map { property ->
                                        mapOf(
                                            "jsName" to nameRules.getName(property),
                                            "getterName" to propertyAdapterName(property, "get"),
                                            "setterName" to propertyAdapterName(property, "set"),
                                            "hasSetter" to (property.setter != null),
                                        )
                                    }
                                    .orEmpty(),
                                "overloadGroups" to (element as? com.here.gluecodium.model.lime.LimeContainer)
                                    ?.functions
                                    ?.filter { it.isStatic && !it.isConstructor }
                                    ?.groupBy { nameRules.getName(it) }
                                    ?.filterValues { it.size > 1 }
                                    ?.map { (jsName, overloads) ->
                                        mapOf(
                                            "jsName" to jsName,
                                            "overloads" to overloads.map { function ->
                                                mapOf(
                                                    "runtimeName" to overloadRuntimeName(function),
                                                    "predicate" to overloadPredicate(function),
                                                )
                                            },
                                        )
                                    }
                                    .orEmpty(),
                            )
                        }
                val duplicateRuntimeExports = runtimeExports.groupBy { it["moduleName"] }.filterValues { it.size > 1 }.keys
                check(duplicateRuntimeExports.isEmpty()) {
                    "Duplicate JavaScript exports in package ${packagePath.joinToString(".")}: " +
                        duplicateRuntimeExports.joinToString(", ")
                }
                GeneratedFile(
                    content,
                    JsNameRules.JS_TARGET_DIRECTORY + directory + java.io.File.separator + "index.d.ts",
                ) to GeneratedFile(
                    TemplateEngine.render(
                        "js/JsRuntimeIndex",
                        mapOf(
                            "runtimeImportPath" to "../".repeat(packagePath.size) + "runtime.mjs",
                            "runtimeExports" to runtimeExports,
                        ),
                        nameResolvers,
                    ),
                    JsNameRules.JS_TARGET_DIRECTORY + directory + java.io.File.separator + "index.mjs",
                )
            }
        val declarationIndexFiles = indexFiles.map { it.first }
        val runtimeIndexFiles = indexFiles.map { it.second }
        val sortedPackagePaths = packageTypes.keys.sortedBy { it.joinToString("/") }
        val exportEntries = sortedPackagePaths.mapIndexed { index, packagePath ->
            val subpath = "./" + packagePath.joinToString("/")
            val relativePath = "./" + packagePath.joinToString("/") + "/index"
            mapOf(
                "subpath" to subpath,
                "typesPath" to "$relativePath.d.ts",
                "importPath" to "$relativePath.mjs",
                "last" to (index == sortedPackagePaths.lastIndex),
            )
        }
        val packageJson =
            TemplateEngine.render(
                "js/JsPackageJson",
                mapOf(
                    "packageName" to jsonString(jsModuleName),
                    "typesPath" to packageTypes.keys.singleOrNull()?.let { packagePath ->
                        (packagePath + "index.d.ts").joinToString("/").let { "./$it" }
                    },
                    "exports" to exportEntries,
                ),
                nameResolvers,
            )
        val tsconfig =
            TemplateEngine.render(
                "js/JsTsconfig",
                emptyMap<String, Any>(),
                nameResolvers,
            )
        val packageMetadataFiles = mutableListOf(
            GeneratedFile(packageJson, JsNameRules.JS_PACKAGE_JSON_FILE),
        )
        if (emitTypeScriptStubs) {
            packageMetadataFiles += GeneratedFile(tsconfig, JsNameRules.JS_TSCONFIG_FILE)
        }
        return (if (emitTypeScriptStubs) declarationIndexFiles else emptyList()) +
            runtimeIndexFiles + packageMetadataFiles
    }

    private fun jsonString(value: String) =
        value
            .replace("\\", "\\\\")
            .replace("\"", "\\\"")
            .replace("\n", "\\n")
            .replace("\r", "\\r")
            .replace("\t", "\\t")

    private fun collectGenericRegistrations(filteredModel: LimeModel): List<Map<String, Any>> {
        val registrations = linkedMapOf<String, Map<String, Any>>()

        fun collect(typeRef: com.here.gluecodium.model.lime.LimeTypeRef) {
            when (val type = typeRef.type) {
                is LimeList -> {
                    collect(type.elementType)
                    if (!requiresJsAdapter(typeRef)) {
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
                else -> Unit
            }
            if (typeRef.isNullable && !requiresJsAdapter(typeRef)) {
                val typeName = resolveGenericRegistrationType(typeRef.type)
                val name = "Optional_${sanitizeRegistrationName(typeName)}"
                registrations.putIfAbsent(name, mapOf("optional" to true, "type" to typeName, "name" to name))
            }
        }

        fun collectFromContainer(container: com.here.gluecodium.model.lime.LimeContainer) {
            container.functions.flatMap { it.parameters.map { parameter -> parameter.typeRef } + it.returnType.typeRef }.forEach(::collect)
            container.properties.map { it.typeRef }.forEach(::collect)
            container.constants.map { it.typeRef }.forEach(::collect)
            container.constructors.flatMap { constructor -> constructor.parameters.map { it.typeRef } }.forEach(::collect)
            (container as? LimeStruct)?.fields?.map { it.typeRef }?.forEach(::collect)
        }

        filteredModel.topElements
            .filterIsInstance<com.here.gluecodium.model.lime.LimeType>()
            .flatMap(::collectEmbindTypes)
            .forEach { type ->
                (type as? com.here.gluecodium.model.lime.LimeContainer)?.let(::collectFromContainer)
            }
        return registrations.values.toList()
    }

    private fun collectGenericRegistrationIncludes(filteredModel: LimeModel): List<Map<String, Any>> {
        val includes = linkedSetOf<Include>()

        fun collect(typeRef: com.here.gluecodium.model.lime.LimeTypeRef) {
            includes += EmbindIncludeResolver(limeReferenceMap, cppNameRules, internalNamespace)
                .resolveElementImports(typeRef)
            when (val type = typeRef.type) {
                is LimeList -> collect(type.elementType)
                is LimeMap -> {
                    collect(type.keyType)
                    collect(type.valueType)
                }
                is LimeSet -> collect(type.elementType)
                else -> Unit
            }
        }

        filteredModel.topElements
            .filterIsInstance<com.here.gluecodium.model.lime.LimeType>()
            .flatMap(::collectEmbindTypes)
            .forEach { type ->
                (type as? com.here.gluecodium.model.lime.LimeContainer)?.let { container ->
                    container.functions.flatMap { it.parameters.map { parameter -> parameter.typeRef } + it.returnType.typeRef }
                        .forEach(::collect)
                    container.properties.map { it.typeRef }.forEach(::collect)
                    container.constants.map { it.typeRef }.forEach(::collect)
                    container.constructors.flatMap { it.parameters.map { parameter -> parameter.typeRef } }.forEach(::collect)
                    (container as? LimeStruct)?.fields?.map { it.typeRef }?.forEach(::collect)
                }
            }

        return includes.map { mapOf("fileName" to it.fileName, "isSystem" to it.isSystem) }
    }

    private fun resolveGenericRegistrationType(type: com.here.gluecodium.model.lime.LimeType): String =
        when (type.actualType) {
            is com.here.gluecodium.model.lime.LimeBasicType -> embindNameResolver.resolveName(type)
            is com.here.gluecodium.model.lime.LimeGenericType -> embindNameResolver.resolveName(type)
            is LimeException -> embindNameResolver.resolveName(type)
            else -> embindNameResolver.resolveFullName(type.actualType as LimeNamedElement)
        }

    private fun containsNullableSet(filteredModel: LimeModel): Boolean {
        fun contains(typeRef: com.here.gluecodium.model.lime.LimeTypeRef): Boolean {
            val type = typeRef.type
            if (typeRef.isNullable && type.actualType is LimeSet) return true
            return type.childTypes.any(::contains)
        }

        return filteredModel.topElements
            .filterIsInstance<com.here.gluecodium.model.lime.LimeType>()
            .flatMap(::collectEmbindTypes)
            .filterIsInstance<com.here.gluecodium.model.lime.LimeContainer>()
            .any { container ->
                container.functions.any { function ->
                    function.parameters.any { contains(it.typeRef) } || contains(function.returnType.typeRef)
                } ||
                    container.properties.any { contains(it.typeRef) } ||
                    container.constants.any { contains(it.typeRef) } ||
                    container.constructors.any { constructor -> constructor.parameters.any { contains(it.typeRef) } } ||
                    (container as? LimeStruct)?.fields?.any { contains(it.typeRef) } == true
            }
    }

    private fun sanitizeRegistrationName(typeName: String) =
        typeName.replace(Regex("[^A-Za-z0-9_]"), "_").trim('_').ifEmpty { "Type" }

    private fun findTopLevelElement(element: LimeNamedElement): LimeNamedElement {
        var current = element
        while (current.path.hasParent) {
            val parent = limeReferenceMap[current.path.parent.toString()] as? LimeNamedElement ?: return current
            current = parent
        }
        return current
    }

    private fun resolveRegisterName(limeElement: LimeNamedElement): String {
        val name = nameRules.getFlattenedName(limeElement)
        val packagePath = limeElement.path.head.joinToString("_")
        return if (packagePath.isNotEmpty()) "${packagePath}_$name" else name
    }

    private fun embindPublicName(type: com.here.gluecodium.model.lime.LimeType): String {
        val jsName = nameRules.getName(type)
        return if (jsName in setOf("InternalError", "BindingError", "UnboundTypeError")) {
            "${resolveRegisterName(type)}Type"
        } else {
            jsName
        }
    }

    // Topologically sorts register names so that every base class appears before its derived
    // classes. A stable sort is used for ties so the output stays deterministic.
    private fun topologicalSort(parents: Map<String, List<String>>): List<String> {
        val visited = mutableSetOf<String>()
        val result = mutableListOf<String>()

        fun visit(name: String) {
            if (name in visited) return
            visited.add(name)
            parents[name].orEmpty().forEach { visit(it) }
            result.add(name)
        }
        parents.keys.sorted().forEach { visit(it) }
        return result
    }

    private fun selectStubTemplate(limeElement: LimeNamedElement) =
        when (limeElement) {
            is com.here.gluecodium.model.lime.LimeTypeAlias -> "js/JsStubTypeAlias"
            is LimeException -> "js/JsStubException"
            is LimeLambda -> "js/JsStubLambda"
            is com.here.gluecodium.model.lime.LimeEnumeration -> "js/JsStubEnumeration"
            is LimeStruct -> "js/JsStubStruct"
            is com.here.gluecodium.model.lime.LimeClass -> "js/JsStubClass"
            is com.here.gluecodium.model.lime.LimeInterface -> "js/JsStubInterface"
            else -> null
        }

    private fun selectEmbindTemplate(limeElement: LimeNamedElement) =
        when (limeElement) {
            is LimeException -> "js/EmbindException"
            is com.here.gluecodium.model.lime.LimeEnumeration -> "js/EmbindEnum"
            is LimeStruct -> "js/EmbindStruct"
            is com.here.gluecodium.model.lime.LimeClass -> "js/EmbindClass"
            is com.here.gluecodium.model.lime.LimeInterface -> "js/EmbindInterface"
            else -> null
        }

    private fun isSupportedConstant(constant: LimeConstant) =
        when (constant.typeRef.type.actualType) {
            is LimeList, is LimeSet, is LimeMap -> false
            else -> true
        }

    /**
     * `@Cpp(Skip)` may only be used on field constructors and constants. Such elements are
     * omitted from the generated C++ API, so the embind binding — which wraps that C++ API —
     * must omit them too, or the binding would fail to compile.
     */
    private fun isCppSkipped(element: LimeNamedElement) =
        (element is LimeFieldConstructor || element is com.here.gluecodium.model.lime.LimeConstant) &&
            element.attributes.have(LimeAttributeType.CPP, SKIP)

    companion object {
        private val logger = Logger.getLogger(JsGenerator::class.java.name)
    }
}
