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

package com.here.genium.generator.cpp;

import com.here.genium.model.common.Include;
import java.io.File;
import java.nio.file.Paths;
import java.util.List;
import java.util.Set;

public final class CppLibraryIncludes {
  // Standard
  public static final Include INT_TYPES = Include.Companion.createSystemInclude("cstdint");
  public static final Include MAP = Include.Companion.createSystemInclude("unordered_map");
  public static final Include MEMORY = Include.Companion.createSystemInclude("memory");
  public static final Include STRING = Include.Companion.createSystemInclude("string");
  public static final Include VECTOR = Include.Companion.createSystemInclude("vector");
  public static final Include NEW = Include.Companion.createSystemInclude("new");
  public static final Include SYSTEM_ERROR = Include.Companion.createSystemInclude("system_error");
  public static final Include LIMITS = Include.Companion.createSystemInclude("limits");
  public static final Include CHRONO = Include.Companion.createSystemInclude("chrono");
  public static final Include SET = Include.Companion.createSystemInclude("unordered_set");

  // Custom
  public static final Include RETURN = Include.Companion.createInternalInclude("Return.h");
  public static final Include ENUM_HASH = Include.Companion.createInternalInclude("EnumHash.h");
  public static final Include OPTIONAL = Include.Companion.createInternalInclude("Optional.h");

  private static final String[] INTERNAL_INCLUDES = {"EnumHash.h", "Return.h", "Optional.h"};

  public static void filterIncludes(Set<Include> includes, List<String> internalNamespace) {
    // Internal includes: need to replace with the internal path
    for (String include : INTERNAL_INCLUDES) {
      if (includes.remove(Include.Companion.createInternalInclude(include))) {
        includes.add(
            Include.Companion.createInternalInclude(
                Paths.get(String.join(File.separator, internalNamespace), include).toString()));
      }
    }
  }
}
