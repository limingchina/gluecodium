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
import com.here.gluecodium.generator.common.GenericImportsCollector
import com.here.gluecodium.generator.common.NameResolver
import com.here.gluecodium.generator.common.templates.TemplateEngine
import com.here.gluecodium.model.lime.LimeClass
import com.here.gluecodium.model.lime.LimeComment
import com.here.gluecodium.model.lime.LimeContainerWithInheritance
import com.here.gluecodium.model.lime.LimeConstant
import com.here.gluecodium.model.lime.LimeEnumeration
import com.here.gluecodium.model.lime.LimeException
import com.here.gluecodium.model.lime.LimeInterface
import com.here.gluecodium.model.lime.LimeLambda
import com.here.gluecodium.model.lime.LimeNamedElement
import com.here.gluecodium.model.lime.LimeStruct
import com.here.gluecodium.model.lime.LimeTypeAlias

internal class JsStubGenerator(
    private val nameRules: JsNameRules,
    private val jsNameResolver: JsNameResolver,
    private val jsModuleName: String,
    private val importsCollector: GenericImportsCollector<JsImport>,
    private val nameResolvers: Map<String, NameResolver>,
    private val isSupportedConstant: (LimeConstant) -> Boolean,
    private val isCppSkipped: (LimeNamedElement) -> Boolean,
) {
    fun generate(elements: List<LimeNamedElement>): List<GeneratedFile> =
        elements.flatMap(::generateFile)

    private fun generateFile(limeElement: LimeNamedElement): List<GeneratedFile> {
        val templateName = selectTemplate(limeElement) ?: return emptyList()
        val selfModulePath = relativeModulePath(
            limeElement.path.head,
            limeElement.path.head,
            nameRules.getName(limeElement),
        )
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
                ) + viewModel(limeElement),
                nameResolvers,
            )
        return listOf(GeneratedFile(content, nameRules.getJsStubFileName(limeElement)))
    }

    private fun relativeModulePath(
        currentPackage: List<String>,
        targetPackage: List<String>,
        targetName: String,
    ): String {
        val commonLength = currentPackage.zip(targetPackage).takeWhile { (current, target) -> current == target }.count()
        val parentPath = "../".repeat(currentPackage.size - commonLength)
        val targetPath = targetPackage.drop(commonLength).joinToString("/")
        return "./" + parentPath + targetPath.takeIf { it.isNotEmpty() }?.let { "$it/" }.orEmpty() + targetName
    }

    private fun viewModel(limeElement: LimeNamedElement): Map<String, Any> {
        val data = mutableMapOf<String, Any>(
            "jsName" to nameRules.getName(limeElement),
            "comment" to limeElement.comment,
            "additionalDescriptionComment" to LimeComment(),
            "hasDocumentation" to hasDocumentation(limeElement.comment),
        )
        val container = limeElement as? com.here.gluecodium.model.lime.LimeContainer
        if (container != null) {
            val inheritedContainer = container as? LimeContainerWithInheritance
            val functions = (container.functions + inheritedContainer?.inheritedFunctions.orEmpty())
                .distinctBy { it.fullName }
            val properties = (container.properties + inheritedContainer?.inheritedProperties.orEmpty())
                .distinctBy { it.fullName }
            data["constructors"] = container.constructors.map(::functionViewModel)
            data["functions"] = functions.map(::functionViewModel)
            data["hasStaticFunctions"] = functions.any { it.isStatic && !it.isConstructor }
            val constants = container.constants
                .filter(isSupportedConstant)
                .filterNot(isCppSkipped)
                .map { constant ->
                    mapOf(
                        "jsName" to nameRules.getName(constant),
                        "jsType" to jsNameResolver.resolveName(constant.typeRef),
                        "comment" to constant.comment,
                        "additionalDescriptionComment" to LimeComment(),
                        "hasDocumentation" to hasDocumentation(constant.comment),
                    )
                }
            data["constants"] = constants
            data["hasConstants"] = constants.isNotEmpty()
            data["constantOwnerName"] = nameRules.getName(limeElement)
            data["parentJsName"] = nameRules.getName(limeElement)
            data["hasInstanceDeclaration"] =
                limeElement is LimeStruct && limeElement.fields.isNotEmpty() ||
                    properties.isNotEmpty() ||
                    functions.any { !it.isStatic || it.isConstructor }
            data["properties"] = properties.map {
                mapOf(
                    "jsName" to nameRules.getName(it),
                    "jsType" to jsNameResolver.resolveName(it.typeRef),
                    "isStatic" to it.isStatic,
                    "comment" to it.comment,
                    "additionalDescriptionComment" to it.additionalDescriptionComment,
                    "hasDocumentation" to
                        (hasDocumentation(it.comment) || hasDocumentation(it.additionalDescriptionComment)),
                )
            }
            data["nestedEnumerations"] = container.enumerations.map { enumeration ->
                mapOf(
                    "jsName" to nameRules.getName(enumeration),
                    "comment" to enumeration.comment,
                    "hasDocumentation" to hasDocumentation(enumeration.comment),
                    "enumerators" to enumeration.enumerators.map { enumerator ->
                        mapOf(
                            "jsName" to nameRules.getName(enumerator),
                            "comment" to enumerator.comment,
                            "additionalDescriptionComment" to LimeComment(),
                            "hasDocumentation" to hasDocumentation(enumerator.comment),
                        )
                    },
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
                    "hasDocumentation" to hasDocumentation(it.comment),
                )
            }
        }
        if (limeElement is LimeEnumeration) {
            data["enumerators"] = limeElement.enumerators.map {
                mapOf(
                    "jsName" to nameRules.getName(it),
                    "comment" to it.comment,
                    "additionalDescriptionComment" to LimeComment(),
                    "hasDocumentation" to hasDocumentation(it.comment),
                )
            }
        }
        return data
    }

    private fun functionViewModel(function: com.here.gluecodium.model.lime.LimeFunction): Map<String, Any> =
        mapOf(
            "jsName" to nameRules.getName(function),
            "comment" to function.comment,
            "hasDocumentation" to hasDocumentation(function),
            "isConstructor" to function.isConstructor,
            "isStatic" to function.isStatic,
            "returnType" to returnType(function),
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

    private fun hasDocumentation(function: com.here.gluecodium.model.lime.LimeFunction): Boolean =
        jsNameResolver.resolveName(function.comment).isNotBlank() ||
            function.parameters.any { jsNameResolver.resolveName(it.comment).isNotBlank() } ||
            jsNameResolver.resolveName(function.returnType.comment).isNotBlank() ||
            (function.thrownType?.comment?.let { jsNameResolver.resolveName(it).isNotBlank() } == true)

    private fun hasDocumentation(comment: LimeComment): Boolean =
        jsNameResolver.resolveName(comment).isNotBlank()

    private fun returnType(function: com.here.gluecodium.model.lime.LimeFunction): String {
        val exception = function.exception ?: return jsNameResolver.resolveName(function.returnType)
        val valueType = if (function.returnType.isVoid) null else jsNameResolver.resolveName(function.returnType)
        val errorType =
            if (exception.errorType.type.actualType is LimeEnumeration) {
                "number"
            } else {
                jsNameResolver.resolveName(exception.errorType)
            }
        return listOfNotNull(valueType?.let { "value?: $it" }, "error?: $errorType")
            .joinToString("; ", prefix = "{ ", postfix = " }")
    }

    private fun selectTemplate(limeElement: LimeNamedElement): String? =
        when (limeElement) {
            is LimeTypeAlias -> "js/JsStubTypeAlias"
            is LimeException -> "js/JsStubException"
            is LimeLambda -> "js/JsStubLambda"
            is LimeEnumeration -> "js/JsStubEnumeration"
            is LimeStruct -> "js/JsStubStruct"
            is LimeClass -> "js/JsStubClass"
            is LimeInterface -> "js/JsStubInterface"
            else -> null
        }
}
