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

import com.here.gluecodium.generator.common.NameRuleSet
import com.here.gluecodium.generator.common.NameRules
import com.here.gluecodium.model.lime.LimeAttributeType.PYTHON
import com.here.gluecodium.model.lime.LimeAttributeValueType.NAME
import com.here.gluecodium.model.lime.LimeElement
import com.here.gluecodium.model.lime.LimeNamedElement
import com.here.gluecodium.model.lime.LimeProperty
import com.here.gluecodium.model.lime.LimeType
import java.io.File

/**
 * Name rules for the Python generator. Resolves file names and platform (Python) names for
 * LIME elements, honouring the `@Python(Name = ...)` attribute.
 */
class PythonNameRules(nameRuleSet: NameRuleSet) : NameRules(nameRuleSet) {
    override fun getName(limeElement: LimeElement) =
        getPlatformName(limeElement as? LimeNamedElement)
            ?: if (limeElement is LimeType && limeElement.path.hasParent) {
                limeElement.path.tail.joinToString("")
            } else {
                super.getName(limeElement)
            }

    override fun getPropertyName(limeProperty: LimeProperty) = getPlatformName(limeProperty) ?: super.getPropertyName(limeProperty)

    /** Resolve the output path of a generated Python source file for the given element. */
    fun getPythonFileName(limeElement: LimeNamedElement): String {
        val packagePath = limeElement.path.head.joinToString(File.separator)
        return PYTHON_TARGET_DIRECTORY + packagePath + File.separator + getName(limeElement) + ".py"
    }

    /** Resolve the output path of a generated pybind11 C++ binding file for the given element. */
    fun getPybind11FileName(limeElement: LimeNamedElement): String {
        val packagePath = limeElement.path.head.joinToString("_")
        return PYBIND11_TARGET_DIRECTORY + packagePath + "_" + getName(limeElement) + ".cpp"
    }

    /** Resolve the output path of a generated Python type-stub (`.pyi`) file for the element. */
    fun getPythonStubFileName(limeElement: LimeNamedElement): String {
        val packagePath = limeElement.path.head.joinToString(File.separator)
        return PYTHON_TARGET_DIRECTORY + packagePath + File.separator + getName(limeElement) + ".pyi"
    }

    /**
     * Resolve the output path of a generated Python source file for the given `.lime` source file.
     * All elements declared in that source file are emitted into a single module named after the
     * file's basename (e.g. `test/Inheritance.lime` -> `python/test/Inheritance.py`), so the
     * generated wrappers match the per-feature import style used by the test harness.
     */
    fun getPythonFileNameForFile(fileName: String, packagePath: String): String {
        val moduleName = File(fileName).nameWithoutExtension
        return PYTHON_TARGET_DIRECTORY + packagePath + File.separator + moduleName + ".py"
    }

    /** Resolve the output path of a generated Python type-stub (`.pyi`) file for the source file. */
    fun getPythonStubFileNameForFile(fileName: String, packagePath: String): String {
        val moduleName = File(fileName).nameWithoutExtension
        return PYTHON_TARGET_DIRECTORY + packagePath + File.separator + moduleName + ".pyi"
    }

    private fun getPlatformName(limeElement: LimeNamedElement?) = limeElement?.attributes?.get(PYTHON, NAME)

    companion object {
        val PYTHON_TARGET_DIRECTORY = "python" + File.separator
        val PYBIND11_TARGET_DIRECTORY = PYTHON_TARGET_DIRECTORY + "pybind11" + File.separator
        val MODULE_INIT_FILE = PYBIND11_TARGET_DIRECTORY + "_module_init.cpp"
    }
}
