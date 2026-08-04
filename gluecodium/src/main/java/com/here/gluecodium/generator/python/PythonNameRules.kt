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

import com.here.gluecodium.generator.common.CommonGeneratorPredicates
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
            ?: sanitizeKeyword(maybePrefixInternal(super.getName(limeElement), limeElement))

    /**
     * Returns the flattened (concatenated) name for pybind11 registration identifiers.
     * Nested types like `Outer.Inner` become `OuterInner` so the resulting C++ function name
     * (e.g. `register_pkg_OuterInner`) is a valid, dot-free identifier. This preserves
     * backward compatibility with the per-type pybind11 binding files.
     *
     * `@Internal` elements are also prefixed with `_` here (not just in [getName]) so that
     * pybind11 file names and `register_*` function names do not collide when an internal
     * type has the same LIME name as a public type (e.g. the `name_clash_overloads` smoke
     * test, where `@Internal class AssetsManager {}` coexists with a public
     * `class AssetsManager {}` in the same package). This mirrors how C++ avoids the
     * collision via `@Cpp("AssetsManagerInternal")`.
     */
    fun getFlattenedName(limeElement: LimeNamedElement): String {
        val platformName = getPlatformName(limeElement)
        if (platformName != null) return sanitizeKeyword(platformName)
        val baseName =
            if (limeElement is LimeType && limeElement.path.hasParent)
                limeElement.path.tail.joinToString("")
            else
                super.getName(limeElement)
        return sanitizeKeyword(maybePrefixInternal(baseName, limeElement))
    }

    override fun getPropertyName(limeProperty: LimeProperty) =
        getPlatformName(limeProperty)
            ?: sanitizeKeyword(maybePrefixInternal(super.getPropertyName(limeProperty), limeProperty))

    /** Resolve the output path of a generated Python source file for the given element. */
    fun getPythonFileName(limeElement: LimeNamedElement): String {
        val packagePath = limeElement.path.head.joinToString(File.separator)
        return PYTHON_TARGET_DIRECTORY + packagePath + File.separator + getName(limeElement) + ".py"
    }

    /** Resolve the output path of a generated pybind11 C++ binding file for the given element. */
    fun getPybind11FileName(limeElement: LimeNamedElement): String {
        val packagePath = limeElement.path.head.joinToString("_")
        return PYBIND11_TARGET_DIRECTORY + packagePath + "_" + getFlattenedName(limeElement) + ".cpp"
    }

    /** Resolve the output path of a generated Python type-stub (`.pyi`) file for the element. */
    fun getPythonStubFileName(limeElement: LimeNamedElement): String {
        val packagePath = limeElement.path.head.joinToString(File.separator)
        return PYTHON_TARGET_DIRECTORY + packagePath + File.separator + getName(limeElement) + ".pyi"
    }

    private fun getPlatformName(limeElement: LimeNamedElement?) = limeElement?.attributes?.get(PYTHON, NAME)

    /**
     * Prepends a single underscore to [name] if [element] is `@Internal` for Python, following
     * PEP 8's convention for non-public API. This makes internal members reachable but clearly
     * signals they are not part of the public API. A `@Python(Name=...)` override (handled by
     * [getPlatformName]) takes priority and bypasses this prefixing.
     */
    private fun maybePrefixInternal(name: String, element: Any): String {
        val namedElement = element as? LimeNamedElement ?: return name
        return if (CommonGeneratorPredicates.isInternal(namedElement, PYTHON)) "_$name" else name
    }

    /**
     * Appends an underscore to any Python hard keyword to avoid SyntaxError in generated code.
     * LIME allows reserved keywords as identifiers via backtick-escaping (e.g. `lambda`),
     * but Python's grammar treats them as unconditioned keywords that cannot be used as
     * parameter or variable names.
     */
    private fun sanitizeKeyword(name: String) = if (name in PYTHON_KEYWORDS) name + "_" else name

    companion object {
        val PYTHON_TARGET_DIRECTORY = "python" + File.separator
        val PYBIND11_TARGET_DIRECTORY = PYTHON_TARGET_DIRECTORY + "pybind11" + File.separator
        val MODULE_INIT_FILE = PYBIND11_TARGET_DIRECTORY + "_module_init.cpp"

        /** Python 3 hard keywords that cannot be used as identifiers. */
        private val PYTHON_KEYWORDS =
            setOf(
                "False", "None", "True", "and", "as", "assert", "async", "await",
                "break", "class", "continue", "def", "del", "elif", "else", "except",
                "finally", "for", "from", "global", "if", "import", "in", "is",
                "lambda", "nonlocal", "not", "or", "pass", "raise", "return", "try",
                "while", "with", "yield",
            )
    }
}
