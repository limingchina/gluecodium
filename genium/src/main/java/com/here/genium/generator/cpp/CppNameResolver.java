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

package com.here.genium.generator.cpp;

import com.here.genium.common.FrancaTypeHelper;
import com.here.genium.generator.common.NameRules;
import com.here.genium.generator.common.VerbatimNameRules;
import com.here.genium.model.franca.FrancaDeploymentModel;
import java.util.HashMap;
import java.util.Map;
import java.util.function.BiFunction;
import lombok.Value;
import org.eclipse.emf.ecore.EObject;
import org.franca.core.franca.*;

public class CppNameResolver {

  private final FrancaDeploymentModel deploymentModel;
  private final Map<String, NamesCacheEntry> namesCache = new HashMap<>();

  @Value
  private static final class NamesCacheEntry {
    private final boolean isExternal;
    private final String shortName;
    private final String fullName;
  }

  public CppNameResolver(final FrancaDeploymentModel deploymentModel) {
    this.deploymentModel = deploymentModel;
  }

  public String getName(final FModelElement francaElement) {
    return getCachedEntry(francaElement).getShortName();
  }

  public String getFullyQualifiedName(final FModelElement francaElement) {
    return getCachedEntry(francaElement).getFullName();
  }

  private NamesCacheEntry getCachedEntry(final FModelElement francaElement) {

    String cacheKey = FrancaTypeHelper.getFullName(francaElement);
    if (!namesCache.containsKey(cacheKey)) {
      resolveNames(cacheKey, francaElement);
    }
    return namesCache.get(cacheKey);
  }

  private void resolveNames(final String cacheKey, final FModelElement francaElement) {

    EObject parentElement = francaElement.eContainer();
    if (parentElement instanceof FTypeCollection && !(parentElement instanceof FInterface)) {
      // A type collection doesn't correspond to any named entity in C++ generated code. So skip it
      // and use the parent FModel instead.
      parentElement = parentElement.eContainer();
    }

    String parentFqn;
    boolean parentIsExternal = false;
    if (parentElement instanceof FModel) {
      parentFqn = "::" + ((FModel) parentElement).getName();
    } else if (parentElement instanceof FModelElement) {
      NamesCacheEntry parentCacheEntry = getCachedEntry((FModelElement) parentElement);
      parentIsExternal = parentCacheEntry.isExternal();
      parentFqn = parentCacheEntry.getFullName();
    } else {
      parentFqn = "";
    }

    boolean isExternal = parentIsExternal || deploymentModel.isExternalType(francaElement);
    String externalName = deploymentModel.getExternalName(francaElement);
    if (externalName != null) {
      namesCache.put(cacheKey, new NamesCacheEntry(isExternal, externalName, externalName));
      return;
    }

    NameRules nameRules = isExternal ? VerbatimNameRules.INSTANCE : CppNameRules.INSTANCE;
    String name = selectNameRule(francaElement).apply(nameRules, francaElement.getName());
    String fullyQualifiedName = parentFqn + "::" + name;
    namesCache.put(cacheKey, new NamesCacheEntry(isExternal, name, fullyQualifiedName));
  }

  private static BiFunction<NameRules, String, String> selectNameRule(
      final FModelElement francaElement) {

    if (francaElement instanceof FField || francaElement instanceof FArgument) {
      return NameRules::getVariableName;
    }
    if (francaElement instanceof FConstantDef || francaElement instanceof FEnumerator) {
      return NameRules::getConstantName;
    }
    if (francaElement instanceof FMethod || francaElement instanceof FAttribute) {
      return NameRules::getFunctionName;
    }

    return NameRules::getTypeName;
  }
}
