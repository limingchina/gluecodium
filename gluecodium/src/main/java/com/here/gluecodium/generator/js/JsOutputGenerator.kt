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
import com.here.gluecodium.model.lime.LimeElement
import com.here.gluecodium.model.lime.LimeModel
import com.here.gluecodium.model.lime.LimeNamedElement

internal class JsOutputGenerator(
    private val nameRules: JsNameRules,
    private val jsNameResolver: JsNameResolver,
    private val embindNameResolver: EmbindNameResolver,
    private val jsModuleName: String,
    private val emitTypeScriptStubs: Boolean,
    private val referenceMap: Map<String, LimeElement>,
    private val embindFileGenerator: JsEmbindFileGenerator,
    private val commonFileGenerator: JsCommonFileGenerator,
) {
    fun generate(
        embindModel: LimeModel,
        stubsModel: LimeModel,
    ): List<GeneratedFile> {
        val nameResolvers =
            mapOf(
                "" to jsNameResolver,
                "Embind" to embindNameResolver,
                "C++" to embindNameResolver,
            )
        val importsCollector =
            GenericImportsCollector(
                JsImportResolver(referenceMap, nameRules),
                collectTypeRefImports = true,
                collectValueImports = false,
                parentTypeFilter = { true },
                collectTypeAliasImports = true,
            )
        val stubFiles =
            if (emitTypeScriptStubs) {
                JsStubGenerator(
                    nameRules,
                    jsNameResolver,
                    jsModuleName,
                    importsCollector,
                    nameResolvers,
                ).generate(stubsModel.topElements.filterIsInstance<LimeNamedElement>())
            } else {
                emptyList()
            }
        val embindFiles =
            embindModel.topElements.flatMap {
                embindFileGenerator.generate(it, nameResolvers, embindModel)
            }
        return stubFiles + embindFiles +
            commonFileGenerator.generate(embindModel, stubsModel, nameResolvers)
    }
}