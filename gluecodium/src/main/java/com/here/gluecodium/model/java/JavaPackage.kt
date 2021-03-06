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

package com.here.gluecodium.model.java

data class JavaPackage(private val packageList: List<String>) {
    val packageNames = packageList.map { it.replace("_", "") }

    override fun toString() = packageNames.joinToString(".")

    @Suppress("unused")
    fun toJniString() = packageNames.joinToString("/")

    fun createChildPackage(additionalPackages: List<String>) =
        JavaPackage(packageNames + additionalPackages)

    companion object {
        val DEFAULT_PACKAGE_NAMES = listOf("com", "example")
        val DEFAULT = JavaPackage(DEFAULT_PACKAGE_NAMES)
    }
}
