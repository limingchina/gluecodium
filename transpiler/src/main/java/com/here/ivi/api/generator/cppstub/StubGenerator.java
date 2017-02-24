package com.here.ivi.api.generator.cppstub;


import com.google.common.collect.Iterables;
import com.here.ivi.api.generator.common.*;
import com.here.ivi.api.generator.common.templates.CppFileTemplate;
import com.here.ivi.api.generator.common.templates.CppNameRules;
import com.here.ivi.api.generator.common.templates.CppTypeCollectionContentTemplate;
import com.here.ivi.api.generator.cppstub.templates.NotifierBodyTemplate;
import com.here.ivi.api.generator.cppstub.templates.NotifierTypeTemplate;
import com.here.ivi.api.model.FrancaModel;
import com.here.ivi.api.model.Includes;
import com.here.ivi.api.model.cppmodel.*;
import navigation.CppStubSpec;
import org.franca.core.franca.FArgument;
import org.franca.core.franca.FBroadcast;
import org.franca.core.franca.FMethod;

import java.util.ArrayList;
import java.util.List;
import java.util.Set;
import java.util.stream.Collectors;

/**
 * This generator will create the stub interfaces that will then be used by the other generators.
 */
public class StubGenerator {

    private final GeneratorSuite<?, ?> suite;
    private final FrancaModel coreModel;
    private final CppNameRules nameRules;

    private final FrancaModel.Interface<? extends CppStubSpec.InterfacePropertyAccessor> iface;
    private final CppModelAccessor<? extends CppStubSpec.InterfacePropertyAccessor> rootModel;


    public StubGenerator(GeneratorSuite<?, ?> suite,
                         FrancaModel<
                                 ? extends CppStubSpec.InterfacePropertyAccessor,
                                 ? extends CppStubSpec.TypeCollectionPropertyAccessor> coreModel,
                         CppNameRules rules,
                         FrancaModel.Interface<? extends CppStubSpec.InterfacePropertyAccessor> iface) {
        this.nameRules = rules;
        this.suite = suite;
        this.coreModel = coreModel;
        this.iface = iface;

        // this is the main type of the file, all namespaces and includes have to be resolved relative to it
        rootModel = new CppModelAccessor<>(iface.fInterface, iface.getModel().fModel, iface.accessor);
    }

    public GeneratedFile generate() {
        CppNamespace model = buildCppModel();

        if (model.isEmpty()) {
            return null;
        }

        String[] packageDesc = nameRules.packageName(iface.getPackage());
        String outputFile = nameRules.interfaceStubTarget(packageDesc, iface);

        // find included files and resolve relative to generated path
        CppIncludeResolver resolver = new CppIncludeResolver(coreModel, iface, nameRules);
        resolver.resolveLazyIncludes(model);

        Object generatorNotice = CppGeneratorHelper.generateGeneratorNotice(suite, iface, outputFile);
        Object innerContent = CppTypeCollectionContentTemplate.generate(model);
        String fileContent = CppFileTemplate.generate(generatorNotice, innerContent).toString();

        return new GeneratedFile(fileContent, outputFile);
    }

    private CppNamespace buildCppModel() {

        String[] packageDesc = nameRules.packageName(iface.getPackage());
        List<CppNamespace> packageNs = CppGeneratorHelper.packageToNamespace(packageDesc);

        CppClass result = new CppClass(iface.getName() + "Stub" );

        // TODO reuse TypeCollectionGenerator to generate types in interface definition

        for (FMethod m : iface.fInterface.getMethods()) {
            CppMethod method = buildStubMethod(m);
            result.methods.add(method);
        }

        for (FBroadcast b : iface.fInterface.getBroadcasts()) {

            String notifierName = NotifierTypeTemplate.generateName(b);
            String notifierVariableName = NotifierTypeTemplate.generateNotifier(b);

            CppMethod method = buildNotifierMethod(b, notifierVariableName);
            CppType notifierType = new CppType(null, NotifierTypeTemplate.generateType(method),
                    CppElements.TypeInfo.Complex, new Includes.SystemInclude("functional"));

            result.usings.add(new CppUsing(notifierName, notifierType));
            result.methods.add(method);
            result.fields.add(new CppField(new CppType(notifierName),
                    notifierVariableName, new CppValue("nullptr")));
        }

        // add to innermost namespace
        Iterables.getLast(packageNs).members.add(result);

        // return outermost namespace
        return Iterables.getFirst(packageNs, null);
    }

    // they will be called from the cpp implementation, and this will then be forwarded in some
    // api specific way to the next level
    private CppMethod buildNotifierMethod(FBroadcast b, String notifierVariableName) {
        CppMethod method = new CppMethod();

        method.name = "notify" + NameHelper.toUpperCamel(b.getName()) +
                NameHelper.toUpperCamel(b.getSelector());

        for (FArgument outArgs : b.getOutArgs()) {
            CppParameter param = new CppParameter();
            param.name = outArgs.getName();
            param.mode = CppParameter.Mode.Input;
            param.type = CppTypeMapper.map(rootModel, outArgs.getType());
            method.inParameters.add(param);
        }

        // add method body template
        method.mbt = new NotifierBodyTemplate(notifierVariableName);

        return method;
    }

    private CppMethod buildStubMethod(FMethod m) {
        CppMethod method = new CppMethod();

        method.name = m.getName() + NameHelper.toUpperCamel(m.getSelector());
        method.returnType = buildStubMethodReturnType(m);
        method.specifiers.add("virtual");

        if (iface.accessor.getConst(m)) {
            // const needs to be before = 0; This smells more than the = 0 below
            method.qualifiers.add(" const");
        }
        method.qualifiers.add(" = 0");

        for (FArgument inArg : m.getInArgs()) {
            CppParameter param = new CppParameter();
            param.name = inArg.getName();
            param.mode = CppParameter.Mode.Input;
            param.type = CppTypeMapper.map(rootModel, inArg.getType());
            method.inParameters.add(param);
        }
        return method;
    }

    private final static Includes.SystemInclude TUPLE_INCLUDE = new Includes.SystemInclude("tuple");

    private CppType buildStubMethodReturnType(FMethod m) {
        List<CppType> returnTypes = new ArrayList<>();

        // TODO do we need to support Errors, instead of ErrorEnum as well - might need to create an inline type
        if (m.getErrorEnum() != null) {
            CppType mapped = CppTypeMapper.mapEnum(rootModel, m.getErrorEnum());
            returnTypes.add(mapped);
        }

        for (FArgument outArg : m.getOutArgs()) {
            CppType mapped = CppTypeMapper.map(rootModel, outArg);
            returnTypes.add(mapped);
        }

        if (!returnTypes.isEmpty()) {
            if (returnTypes.size() == 1) {
                return returnTypes.get(0);
            } else {
                List<String> names = returnTypes.stream().map(t -> t.name).collect(Collectors.toList());
                Set<Includes.Include> includes = returnTypes.stream()
                        .flatMap(t -> t.includes.stream())
                        .collect(Collectors.toSet());
                includes.add(TUPLE_INCLUDE);

                // TODO still too much string magic!!
                // TODO missing type definition
                return new CppType(
                        null,
                        "std::tuple< " + String.join(", ", names) + " >",
                        CppElements.TypeInfo.Complex,
                        includes );
            }
        }

        return CppType.Void;
    }
}
