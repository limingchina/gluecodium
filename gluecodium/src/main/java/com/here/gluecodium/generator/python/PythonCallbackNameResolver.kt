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

package com.here.gluecodium.generator.python

import com.here.gluecodium.generator.common.NameResolver
import com.here.gluecodium.model.lime.LimeNamedElement

/** Names private trampoline adapters by the complete LIME path, including overload signatures. */
internal class PythonCallbackNameResolver : NameResolver {
    override fun resolveName(element: Any): String {
        val path = (element as LimeNamedElement).path.toString()
        return "__gluecodium_callback_" + path.toByteArray(Charsets.UTF_8).joinToString("") { "%02x".format(it) }
    }

    override fun resolveGetterName(element: Any) = resolveName(element) + "_get"

    override fun resolveSetterName(element: Any) = resolveName(element) + "_set"
}
