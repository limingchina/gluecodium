/*
 * Copyright (C) 2016-2018 HERE Europe B.V.
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

package com.here.genium.model.swift;

import java.util.List;
import lombok.Builder;
import lombok.Singular;

public final class SwiftEnum extends SwiftType {

  public final List<SwiftEnumItem> items;

  @Builder
  private SwiftEnum(
      final String name,
      final SwiftVisibility visibility,
      final String comment,
      @Singular final List<SwiftEnumItem> items) {
    super(name, visibility, TypeCategory.ENUM, null, name, false);
    this.comment = comment;
    this.items = items;
  }

  public static SwiftEnum.SwiftEnumBuilder builder(String name) {
    return new SwiftEnum.SwiftEnumBuilder().name(name);
  }
}