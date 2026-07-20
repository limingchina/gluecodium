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

import com.here.gluecodium.common.LimeLogger
import com.here.gluecodium.model.lime.LimeContainer
import com.here.gluecodium.model.lime.LimeContainerWithInheritance
import com.here.gluecodium.model.lime.LimeElement
import com.here.gluecodium.model.lime.LimeFunction
import com.here.gluecodium.model.lime.LimeNamedElement
import com.here.gluecodium.model.lime.LimeSignatureResolver

/**
 * Validate functions and constructors against overloading.
 *
 * The Python wrapper layer now supports overloaded method names: it emits a single generic
 * `*args, **kwargs` dispatcher per resolved name and forwards to the native pybind11 binding, which
 * uses `py::overload_cast<...>()` to pick the right C++ overload. The only case that genuinely
 * cannot be bound is when two overloads resolve to the *same C++ signature* (same parameter types),
 * because pybind11 then has no way to disambiguate them. For those we still warn and point users at
 * `@Python(Name = ...)` as the escape hatch.
 */
internal class PythonOverloadsValidator(
    private val nameResolver: PythonNameResolver,
    private val signatureResolver: LimeSignatureResolver,
    private val logger: LimeLogger,
    private val werror: Boolean,
) {
    private val logFunction: LimeLogger.(LimeNamedElement, String) -> Unit =
        if (werror) LimeLogger::error else LimeLogger::warning

    fun validate(limeElements: Collection<LimeElement>): Boolean {
        val validationResults = limeElements.filterIsInstance<LimeContainer>().map { validateContainer(it) }
        return !werror || !validationResults.contains(false)
    }

    private fun validateContainer(limeContainer: LimeContainer): Boolean {
        val allFunctions =
            limeContainer.functions +
                ((limeContainer as? LimeContainerWithInheritance)?.inheritedFunctions ?: emptyList())
        val constructors = allFunctions.filter { it.isConstructor }

        // Group by the *Python* name: these are the overloads the wrapper collapses into one
        // dispatcher. They are fine as long as the C++ layer can still tell them apart by signature.
        val overloadedFunctions =
            (allFunctions - constructors.toSet())
                .groupBy { nameResolver.resolveName(it) }
                .filter { it.value.size > 1 }

        // Only groups that contain a genuine C++ signature clash are unbindable.
        val ambiguousFunctions =
            overloadedFunctions.filter { (_, functions) ->
                functions.any { signatureResolver.hasSignatureClash(it, functions) }
            }
        ambiguousFunctions.forEach { (pythonName, functions) ->
            val pathsString = functions.map { it.path.toString() }.sorted().joinToString()
            logger.logFunction(
                functions.first(),
                "Python method '$pythonName' resolves to ambiguous C++ overloads in $pathsString; " +
                    "use @Python(Name = ...) to give the overloads distinct Python names",
            )
        }

        return ambiguousFunctions.isEmpty()
    }
}
