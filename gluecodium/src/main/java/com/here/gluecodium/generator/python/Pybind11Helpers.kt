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

import com.here.gluecodium.model.lime.LimeAttributeType.PYTHON
import com.here.gluecodium.model.lime.LimeAttributeValueType
import com.here.gluecodium.model.lime.LimeClass
import com.here.gluecodium.model.lime.LimeContainerWithInheritance
import com.here.gluecodium.model.lime.LimeInterface
import com.here.gluecodium.model.lime.LimeNamedElement

/**
 * Helper utilities for the pybind11 binding generator. These are small, pure functions used by the
 * binding templates (via the name resolvers / predicates) to decide how a C++ type should be
 * wrapped.
 */
internal object Pybind11Helpers {
    /** Whether a container needs a trampoline class (i.e. it can be subclassed from Python). */
    fun needsTrampoline(limeElement: LimeNamedElement): Boolean =
        when (limeElement) {
            is LimeInterface -> true
            is LimeClass -> limeElement.isOpen || limeElement.parents.isNotEmpty()
            else -> false
        }

    /** The name of the generated trampoline class for a container, or `null` if not needed. */
    fun trampolineClassName(limeElement: LimeNamedElement): String? =
        if (needsTrampoline(limeElement)) {
            (limeElement as LimeContainerWithInheritance).let { nameCacheName(it) }
        } else {
            null
        }

    private fun nameCacheName(limeElement: LimeNamedElement): String =
        limeElement.attributes.get(PYTHON, LimeAttributeValueType.NAME) ?: limeElement.name

    /** Whether the element is marked `@Python(Internal)`. */
    fun isInternal(limeElement: LimeNamedElement) = limeElement.attributes.have(PYTHON, LimeAttributeValueType.INTERNAL)
}
