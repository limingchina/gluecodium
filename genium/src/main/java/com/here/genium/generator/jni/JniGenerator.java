/*
 * Copyright (c) 2016-2018 HERE Europe B.V.
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

package com.here.genium.generator.jni;

import com.here.genium.common.FrancaTypeHelper;
import com.here.genium.generator.common.AbstractGenerator;
import com.here.genium.generator.common.modelbuilder.FrancaTreeWalker;
import com.here.genium.generator.cpp.CppModelBuilder;
import com.here.genium.generator.cpp.CppNameResolver;
import com.here.genium.generator.cpp.CppTypeMapper;
import com.here.genium.generator.cpp.CppValueMapper;
import com.here.genium.generator.java.JavaModelBuilder;
import com.here.genium.generator.java.JavaTypeMapper;
import com.here.genium.model.common.Include;
import com.here.genium.model.common.ModelElement;
import com.here.genium.model.cpp.CppIncludeResolver;
import com.here.genium.model.franca.DefinedBy;
import com.here.genium.model.franca.FrancaDeploymentModel;
import com.here.genium.model.java.*;
import com.here.genium.model.jni.JniContainer;
import java.util.*;
import java.util.stream.Collectors;
import org.franca.core.franca.FTypeCollection;

public final class JniGenerator extends AbstractGenerator {

  private static final JavaPackage ANDROID_OS_PACKAGE =
      new JavaPackage(Arrays.asList("android", "os"));
  private static final JavaPackage ANDROID_SUPPORT_ANNOTATION_PACKAGE =
      new JavaPackage(Arrays.asList("android", "support", "annotation"));
  private static final JavaType PARCELABLE =
      new JavaCustomType(
          "Parcelable",
          null,
          ANDROID_OS_PACKAGE.getPackageNames(),
          Arrays.asList(
              new JavaImport("Parcelable", ANDROID_OS_PACKAGE),
              new JavaImport("Parcel", ANDROID_OS_PACKAGE)));
  private static final JavaType NON_NULL =
      new JavaCustomType("NonNull", ANDROID_SUPPORT_ANNOTATION_PACKAGE);
  private static final JavaType NULLABLE =
      new JavaCustomType("Nullable", ANDROID_SUPPORT_ANNOTATION_PACKAGE);

  private final FrancaDeploymentModel deploymentModel;
  private final List<String> additionalIncludes;
  private final FrancaTypeHelper.ErrorEnumFilter errorEnumFilter;
  private final boolean enableAndroidFeatures;
  private final String internalNamespace;
  private final CppIncludeResolver cppIncludeResolver;
  private final CppNameResolver cppNameResolver;

  public JniGenerator(
      final FrancaDeploymentModel deploymentModel,
      final List<String> packageList,
      final List<String> additionalIncludes,
      final FrancaTypeHelper.ErrorEnumFilter errorEnumFilter,
      final boolean enableAndroidFeatures,
      final String internalNamespace,
      final List<String> rootNamespace) {
    super(packageList);
    this.deploymentModel = deploymentModel;
    this.additionalIncludes = additionalIncludes;
    this.errorEnumFilter = errorEnumFilter;
    this.enableAndroidFeatures = enableAndroidFeatures;
    this.internalNamespace = internalNamespace;
    this.cppIncludeResolver = new CppIncludeResolver(deploymentModel, rootNamespace);
    this.cppNameResolver = new CppNameResolver(deploymentModel, rootNamespace);
  }

  public Collection<ModelElement> generateModel(final FTypeCollection francaTypeCollection) {

    JavaPackage basePackage = new JavaPackage(basePackages);
    JavaModelBuilder javaBuilder =
        new JavaModelBuilder(
            deploymentModel,
            basePackage.createChildPackage(DefinedBy.getPackages(francaTypeCollection)),
            new JavaTypeMapper(
                basePackage,
                deploymentModel,
                enableAndroidFeatures ? PARCELABLE : null,
                enableAndroidFeatures ? NON_NULL : null,
                enableAndroidFeatures ? NULLABLE : null),
            errorEnumFilter);

    CppTypeMapper typeMapper =
        new CppTypeMapper(cppIncludeResolver, cppNameResolver, internalNamespace);
    CppValueMapper valueMapper = new CppValueMapper(deploymentModel, cppNameResolver);
    CppModelBuilder cppBuilder =
        new CppModelBuilder(deploymentModel, typeMapper, valueMapper, cppNameResolver);
    JniModelBuilder jniBuilder =
        new JniModelBuilder(deploymentModel, javaBuilder, cppBuilder, cppIncludeResolver);

    FrancaTreeWalker treeWalker =
        new FrancaTreeWalker(Arrays.asList(javaBuilder, cppBuilder, jniBuilder));
    treeWalker.walkTree(francaTypeCollection);

    JniContainer jniContainer = jniBuilder.getFinalResult(JniContainer.class);
    jniContainer.getIncludes().addAll(getIncludes(jniContainer));

    List<ModelElement> results = new LinkedList<>(javaBuilder.getFinalResults());
    results.add(jniContainer);

    return results;
  }

  private List<Include> getIncludes(final JniContainer jniContainer) {

    List<String> includes = new LinkedList<>();
    if (jniContainer.isFrancaInterface()) {
      includes.add(JniNameRules.getHeaderFileName(JniNameRules.getJniClassFileName(jniContainer)));
    }

    includes.addAll(additionalIncludes);

    return includes
        .stream()
        .map(Include.Companion::createInternalInclude)
        .collect(Collectors.toList());
  }
}
