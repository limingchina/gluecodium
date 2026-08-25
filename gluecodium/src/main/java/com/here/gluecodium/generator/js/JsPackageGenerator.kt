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

import com.here.gluecodium.generator.common.GeneratedFile
import com.here.gluecodium.generator.common.NameResolver
import com.here.gluecodium.generator.common.templates.TemplateEngine
import com.here.gluecodium.model.lime.LimeClass
import com.here.gluecodium.model.lime.LimeConstant
import com.here.gluecodium.model.lime.LimeContainer
import com.here.gluecodium.model.lime.LimeEnumeration
import com.here.gluecodium.model.lime.LimeFunction
import com.here.gluecodium.model.lime.LimeInterface
import com.here.gluecodium.model.lime.LimeModel
import com.here.gluecodium.model.lime.LimeNamedElement
import com.here.gluecodium.model.lime.LimeProperty
import com.here.gluecodium.model.lime.LimeStruct
import com.here.gluecodium.model.lime.LimeType
import java.io.File

internal class JsPackageGenerator(
    private val nameRules: JsNameRules,
    private val jsModuleName: String,
    private val emitTypeScriptStubs: Boolean,
    private val nameResolvers: Map<String, NameResolver>,
    private val collectEmbindTypes: (LimeType) -> List<LimeType>,
    private val isSupportedConstant: (LimeConstant) -> Boolean,
    private val isCppSkipped: (LimeNamedElement) -> Boolean,
    private val propertyAdapterName: (LimeProperty, String) -> String,
    private val overloadRuntimeName: (LimeFunction) -> String,
    private val structFunctionRuntimeName: (LimeFunction) -> String,
    private val overloadPredicate: (LimeFunction) -> String,
    private val instanceOverloadGroups: (LimeType, LimeModel) -> List<Map<String, Any>>,
) {
    fun generate(filteredModel: LimeModel): List<GeneratedFile> {
        val packageTypes =
            filteredModel.topElements
                .filterIsInstance<LimeNamedElement>()
                .groupBy { it.path.head }
                .toSortedMap(compareBy { it.joinToString(".") })
        val indexFiles = packageTypes.map { (packagePath, elements) ->
            packageIndexFiles(packagePath, elements, filteredModel)
        }
        val declarationIndexFiles = indexFiles.map { it.first }
        val runtimeIndexFiles = indexFiles.map { it.second }
        val packageMetadataFiles = packageMetadataFiles(packageTypes.keys)
        return (if (emitTypeScriptStubs) declarationIndexFiles else emptyList()) +
            runtimeIndexFiles + packageMetadataFiles
    }

    private fun packageIndexFiles(
        packagePath: List<String>,
        elements: List<LimeNamedElement>,
        filteredModel: LimeModel,
    ): Pair<GeneratedFile, GeneratedFile> {
        val exports =
            elements
                .sortedBy { nameRules.getName(it) }
                .map { mapOf("moduleName" to nameRules.getName(it)) }
        val directory = packagePath.joinToString(File.separator)
        val declarationFile =
            GeneratedFile(
                TemplateEngine.render("js/JsIndex", mapOf("exports" to exports), nameResolvers),
                JsNameRules.JS_TARGET_DIRECTORY + directory + File.separator + "index.d.ts",
            )
        val runtimeExports = runtimeExports(elements, filteredModel)
        val duplicateRuntimeExports = runtimeExports.groupBy { it["moduleName"] }.filterValues { it.size > 1 }.keys
        check(duplicateRuntimeExports.isEmpty()) {
            "Duplicate JavaScript exports in package ${packagePath.joinToString(".")}: " +
                duplicateRuntimeExports.joinToString(", ")
        }
        val runtimeFile =
            GeneratedFile(
                TemplateEngine.render(
                    "js/JsRuntimeIndex",
                    mapOf(
                        "runtimeImportPath" to "../".repeat(packagePath.size) + "runtime.mjs",
                        "runtimeExports" to runtimeExports,
                    ),
                    nameResolvers,
                ),
                JsNameRules.JS_TARGET_DIRECTORY + directory + File.separator + "index.mjs",
            )
        return declarationFile to runtimeFile
    }

    private fun runtimeExports(
        elements: List<LimeNamedElement>,
        filteredModel: LimeModel,
    ): List<Map<String, Any>> {
        val runtimeElements =
            elements
                .filterIsInstance<LimeType>()
                .flatMap(collectEmbindTypes)
                .filter { it is LimeClass || it is LimeInterface || it is LimeStruct || it is LimeEnumeration }
                .distinctBy { it.fullName }
                .sortedWith(compareBy({ nameRules.getName(it) }, { it.fullName }))
        val preferredNameCounts =
            runtimeElements
                .filter { it.path.hasParent }
                .groupingBy { nameRules.getName(it) }
                .eachCount()
        val moduleNames = mutableSetOf<String>()
        return runtimeElements.map { element ->
            val preferredName = nameRules.getName(element)
            val preferredModuleName =
                if (element.path.hasParent && (preferredNameCounts[preferredName] ?: 0) > 1) {
                    nameRules.getFlattenedName(element)
                } else {
                    preferredName
                }
            val moduleName = uniqueModuleName(element, preferredModuleName, moduleNames)
            moduleNames += moduleName
            mapOf(
                "moduleName" to moduleName,
                "runtimeName" to nameRules.getEmbindRuntimeName(element),
                "isStruct" to (element is LimeStruct),
                "constants" to (element as? LimeContainer)
                    ?.constants
                    ?.filter(isSupportedConstant)
                    ?.filterNot(isCppSkipped)
                    ?.map { constant ->
                        mapOf(
                            "jsName" to nameRules.getName(constant),
                            "runtimeName" to constantRuntimeName(constant),
                        )
                    }
                    .orEmpty(),
                "properties" to (element as? LimeContainer)
                    ?.properties
                    ?.filter { it.isStatic }
                    ?.map { property ->
                        mapOf(
                            "jsName" to nameRules.getName(property),
                            "getterName" to propertyAdapterName(property, "get"),
                            "setterName" to propertyAdapterName(property, "set"),
                            "hasSetter" to (property.setter != null),
                        )
                    }
                    .orEmpty(),
                "structFunctions" to (element as? LimeStruct)
                    ?.functions
                    ?.filter { it.isStatic && !it.isConstructor }
                    ?.filter { function ->
                        val jsName = nameRules.getName(function)
                        element.functions.count { nameRules.getName(it) == jsName && it.isStatic && !it.isConstructor } == 1
                    }
                    ?.map { function ->
                        mapOf(
                            "jsName" to nameRules.getName(function),
                            "runtimeName" to structFunctionRuntimeName(function),
                        )
                    }
                    .orEmpty(),
                "overloadGroups" to (element as? LimeContainer)
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
                "instanceOverloadGroups" to
                    if (element is LimeStruct) emptyList() else instanceOverloadGroups(element, filteredModel),
                "thrownFunctions" to thrownFunctions(element),
            )
        }
    }

    private fun uniqueModuleName(
        element: LimeNamedElement,
        preferredName: String,
        usedNames: Set<String>,
    ): String {
        if (preferredName !in usedNames) return preferredName
        val flattenedName = nameRules.getFlattenedName(element)
        if (flattenedName !in usedNames) return flattenedName
        return nameRules.getEmbindRuntimeName(element)
    }

    private fun thrownFunctions(element: LimeType): List<Map<String, Any>> {
        val container = element as? LimeContainer ?: return emptyList()
        return container.functions
            .filter { it.exception != null }
            .filterNot { element is LimeStruct && !it.isStatic }
            .map { function ->
                mapOf(
                    "jsName" to nameRules.getName(function),
                    "runtimeName" to if (function.isStatic || !isOverloaded(function, element)) nameRules.getName(function) else overloadRuntimeName(function),
                    "structRuntimeName" to structFunctionRuntimeName(function),
                    "ownerRuntimeName" to nameRules.getEmbindRuntimeName(element),
                    "isStatic" to function.isStatic,
                    "isStruct" to (element is LimeStruct),
                    "exceptionName" to nameRules.getName(function.exception!!),
                )
            }
    }

    private fun isOverloaded(function: LimeFunction, element: LimeType): Boolean {
        val container = element as? LimeContainer ?: return false
        return container.functions.count { !it.isConstructor && nameRules.getName(it) == nameRules.getName(function) } > 1
    }

    private fun packageMetadataFiles(packagePaths: Set<List<String>>): List<GeneratedFile> {
        val sortedPackagePaths = packagePaths.sortedBy { it.joinToString("/") }
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
                    "typesPath" to packagePaths.singleOrNull()?.let { packagePath ->
                        (packagePath + "index.d.ts").joinToString("/").let { "./$it" }
                    },
                    "exports" to exportEntries,
                ),
                nameResolvers,
            )
        val files = mutableListOf(GeneratedFile(packageJson, JsNameRules.JS_PACKAGE_JSON_FILE))
        if (emitTypeScriptStubs) {
            val tsconfig = TemplateEngine.render("js/JsTsconfig", emptyMap<String, Any>(), nameResolvers)
            files += GeneratedFile(tsconfig, JsNameRules.JS_TSCONFIG_FILE)
        }
        return files
    }

    private fun constantRuntimeName(constant: LimeConstant) =
        "gluecodium_constant_${constant.fullName.replace(".", "__")}"

    private fun jsonString(value: String) =
        value
            .replace("\\", "\\\\")
            .replace("\"", "\\\"")
            .replace("\n", "\\n")
            .replace("\r", "\\r")
            .replace("\t", "\\t")
}
