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

import com.here.gluecodium.generator.common.CommonGeneratorPredicates
import com.here.gluecodium.generator.common.NameRuleSet
import com.here.gluecodium.generator.common.NameRules
import com.here.gluecodium.model.lime.LimeAttributeType.JS
import com.here.gluecodium.model.lime.LimeAttributeValueType.NAME
import com.here.gluecodium.model.lime.LimeElement
import com.here.gluecodium.model.lime.LimeNamedElement
import com.here.gluecodium.model.lime.LimeType
import java.io.File

/**
 * Name rules for the JS generator. Resolves file names and platform (JS/TS) names for LIME
 * elements, honouring the `@Js(Name = ...)` attribute.
 */
class JsNameRules(nameRuleSet: NameRuleSet) : NameRules(nameRuleSet) {
    override fun getName(limeElement: LimeElement) =
        getPlatformName(limeElement as? LimeNamedElement)
            ?: super.getName(limeElement)

    /**
     * Returns the flattened name for embind registration identifiers.
     * Nested types like `Outer.Inner` become `Outer_Inner` so the resulting C++ function name
     * is a valid, dot-free identifier that cannot collide with a top-level `OuterInner` type.
     */
    fun getFlattenedName(limeElement: LimeNamedElement): String {
        val platformName = getPlatformName(limeElement)
        if (platformName != null) return platformName
        val baseName =
            if (limeElement is LimeType && limeElement.path.hasParent) {
                limeElement.path.tail.joinToString("_")
            } else {
                super.getName(limeElement)
            }
        return baseName
    }

    /**
     * Returns the private, globally unique name used by embind at runtime. The name is based on
     * the canonical Lime path rather than a platform rename, so two packages may expose the same
     * public leaf name without colliding in the shared Emscripten module.
     */
    fun getEmbindRuntimeName(limeElement: LimeNamedElement): String {
        val path = limeElement.fullName
            .split('.')
            .joinToString("__") { component -> component.replace(Regex("[^A-Za-z0-9_]"), "_") }
        return "gluecodium__$path"
    }

    /** Resolve the output path of a generated TypeScript declaration stub for the given element. */
    fun getJsStubFileName(limeElement: LimeNamedElement): String {
        val packagePath = limeElement.path.head.joinToString(File.separator)
        return JS_TARGET_DIRECTORY + packagePath + File.separator + getName(limeElement) + ".d.ts"
    }

    /** Resolve the output path of a generated embind C++ binding file for the given element. */
    fun getEmbindFileName(limeElement: LimeNamedElement): String {
        val packagePath = limeElement.path.head.joinToString("_")
        return EMBIND_TARGET_DIRECTORY + packagePath + "_" + getFlattenedName(limeElement) + ".cpp"
    }

    private fun getPlatformName(limeElement: LimeNamedElement?) = limeElement?.attributes?.get(JS, NAME)

    companion object {
        val JS_TARGET_DIRECTORY = "js" + File.separator
        val EMBIND_TARGET_DIRECTORY = JS_TARGET_DIRECTORY + "embind" + File.separator
        val MODULE_INIT_FILE = EMBIND_TARGET_DIRECTORY + "_module_init.cpp"
        val WRAPPER_RUNTIME_FILE = JS_TARGET_DIRECTORY + "WrapperRuntime.mjs"
        val MODULE_RUNTIME_FILE = JS_TARGET_DIRECTORY + "runtime.mjs"
        val JS_PACKAGE_JSON_FILE = JS_TARGET_DIRECTORY + "package.json"
        val JS_TSCONFIG_FILE = JS_TARGET_DIRECTORY + "tsconfig.json"

        fun isInternal(element: LimeNamedElement) = CommonGeneratorPredicates.isInternal(element, JS)
    }
}
