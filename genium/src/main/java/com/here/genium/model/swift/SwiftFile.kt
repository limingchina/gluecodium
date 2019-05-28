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

package com.here.genium.model.swift;

import java.util.LinkedList;
import java.util.List;
import java.util.function.Function;
import java.util.stream.Stream;
import org.jetbrains.annotations.NotNull;

public final class SwiftFile extends SwiftModelElement {

  public final List<SwiftClass> classes = new LinkedList<>();
  public final List<SwiftStruct> structs = new LinkedList<>();
  public final List<SwiftEnum> enums = new LinkedList<>();
  public final List<SwiftTypeDef> typeDefs = new LinkedList<>();
  public final List<SwiftArray> arrays = new LinkedList<>();
  public final List<SwiftDictionary> dictionaries = new LinkedList<>();
  @NotNull public final String fileName;

  public SwiftFile(@NotNull String fileName) {
    super("");
    this.fileName = fileName;
  }

  public boolean isEmpty() {
    return classes.isEmpty()
        && structs.isEmpty()
        && enums.isEmpty()
        && arrays.isEmpty()
        && dictionaries.isEmpty();
  }

  @Override
  public Stream<SwiftModelElement> stream() {
    return Stream.of(
            super.stream(),
            classes.stream(),
            structs.stream(),
            enums.stream(),
            typeDefs.stream(),
            arrays.stream(),
            dictionaries.stream())
        .flatMap(Function.identity());
  }
}