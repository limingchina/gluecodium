/*
 * Copyright (C) 2016-2019 HERE Europe B.V.
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

package com.here.genium.generator.swift

import com.here.genium.generator.common.NameHelper
import com.here.genium.generator.common.NameRuleSet
import com.here.genium.generator.common.NameRuleSet.Companion.ignore2
import com.here.genium.generator.common.NameRules
import com.here.genium.model.lime.LimeContainer
import java.io.File

class SwiftNameRules(nameRuleSet: NameRuleSet = defaultNameRuleSet) : NameRules(nameRuleSet) {
    fun getImplementationFileName(limeContainer: LimeContainer) =
        (TARGET_DIRECTORY +
                limeContainer.path.head.joinToString(File.separator) +
                File.separator +
                getName(limeContainer) +
                ".swift")

    companion object {
        val defaultNameRuleSet = NameRuleSet(
            getFieldName = NameHelper::toLowerCamelCase,
            getParameterName = NameHelper::toLowerCamelCase,
            getConstantName = NameHelper::toLowerCamelCase,
            getEnumeratorName = NameHelper::toLowerCamelCase,
            getMethodName = ignore2(NameHelper::toLowerCamelCase),
            getPropertyName = { name: String, isBoolean: Boolean ->
                when {
                    isBoolean -> "is" + NameHelper.toUpperCamelCase(name)
                    else -> NameHelper.toLowerCamelCase(name)
                }
            },
            getTypeName = NameHelper::toUpperCamelCase
        )

        val TARGET_DIRECTORY = "swift" + File.separator
    }
}
